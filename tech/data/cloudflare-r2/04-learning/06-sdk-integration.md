# AWS SDK, boto3 통합

## 개요

R2는 S3 API와 100% 호환되므로 AWS SDK를 그대로 사용할 수 있습니다. 엔드포인트만 R2로 변경하면 됩니다.

### 지원 SDK

```
공식 지원:
├── JavaScript/TypeScript (@aws-sdk/client-s3)
├── Python (boto3)
├── Go (aws-sdk-go-v2)
├── Java (AWS SDK for Java)
├── Ruby (aws-sdk-ruby)
├── PHP (aws-sdk-php)
├── .NET (AWSSDK.S3)
└── Rust (aws-sdk-rust)
```

---

## Python (boto3)

### 설치 및 설정

```bash
pip install boto3
```

### 기본 클라이언트 설정

```python
import boto3
from botocore.config import Config

# R2 클라이언트 생성
r2 = boto3.client(
    's3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>',
    config=Config(
        signature_version='s3v4',
        retries={'max_attempts': 3}
    )
)

# 또는 리소스 사용
r2_resource = boto3.resource(
    's3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>'
)
```

### 환경 변수로 설정

```bash
# .env 또는 환경 변수
export R2_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
export R2_ACCESS_KEY_ID=<ACCESS_KEY>
export R2_SECRET_ACCESS_KEY=<SECRET_KEY>
```

```python
import os
import boto3

r2 = boto3.client(
    's3',
    endpoint_url=os.environ['R2_ENDPOINT_URL'],
    aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY']
)
```

### 유틸리티 클래스

```python
# r2_client.py
import boto3
from botocore.config import Config
from typing import Optional, BinaryIO, Generator
import os

class R2Client:
    def __init__(
        self,
        account_id: str = None,
        access_key: str = None,
        secret_key: str = None
    ):
        self.endpoint_url = f"https://{account_id or os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
        self.client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=access_key or os.environ['R2_ACCESS_KEY_ID'],
            aws_secret_access_key=secret_key or os.environ['R2_SECRET_ACCESS_KEY'],
            config=Config(signature_version='s3v4')
        )

    def upload_file(self, bucket: str, key: str, file_path: str,
                    content_type: str = None) -> dict:
        """파일 업로드"""
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type

        self.client.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
        return {'bucket': bucket, 'key': key}

    def upload_bytes(self, bucket: str, key: str, data: bytes,
                     content_type: str = 'application/octet-stream') -> dict:
        """바이트 데이터 업로드"""
        self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType=content_type
        )
        return {'bucket': bucket, 'key': key}

    def download_file(self, bucket: str, key: str, file_path: str) -> None:
        """파일 다운로드"""
        self.client.download_file(bucket, key, file_path)

    def download_bytes(self, bucket: str, key: str) -> bytes:
        """바이트 데이터 다운로드"""
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()

    def delete(self, bucket: str, key: str) -> None:
        """객체 삭제"""
        self.client.delete_object(Bucket=bucket, Key=key)

    def exists(self, bucket: str, key: str) -> bool:
        """객체 존재 확인"""
        try:
            self.client.head_object(Bucket=bucket, Key=key)
            return True
        except:
            return False

    def list_objects(self, bucket: str, prefix: str = '',
                     max_keys: int = 1000) -> Generator[dict, None, None]:
        """객체 목록 조회 (페이지네이션)"""
        paginator = self.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(
            Bucket=bucket,
            Prefix=prefix,
            PaginationConfig={'MaxItems': max_keys}
        ):
            for obj in page.get('Contents', []):
                yield {
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'modified': obj['LastModified']
                }

    def generate_presigned_url(self, bucket: str, key: str,
                               expiration: int = 3600,
                               method: str = 'get_object') -> str:
        """Presigned URL 생성"""
        return self.client.generate_presigned_url(
            method,
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration
        )


# 사용 예시
if __name__ == '__main__':
    r2 = R2Client()

    # 업로드
    r2.upload_file('my-bucket', 'test.txt', './local-file.txt')

    # 다운로드
    data = r2.download_bytes('my-bucket', 'test.txt')
    print(data.decode())

    # 목록 조회
    for obj in r2.list_objects('my-bucket', prefix='images/'):
        print(obj)
```

### 비동기 클라이언트 (aioboto3)

```bash
pip install aioboto3
```

```python
import aioboto3
import asyncio

async def main():
    session = aioboto3.Session()

    async with session.client(
        's3',
        endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
        aws_access_key_id='<ACCESS_KEY>',
        aws_secret_access_key='<SECRET_KEY>'
    ) as r2:
        # 업로드
        await r2.put_object(
            Bucket='my-bucket',
            Key='async-test.txt',
            Body=b'Hello async!'
        )

        # 다운로드
        response = await r2.get_object(Bucket='my-bucket', Key='async-test.txt')
        content = await response['Body'].read()
        print(content.decode())

        # 병렬 업로드
        files = [('file1.txt', b'content1'), ('file2.txt', b'content2')]
        tasks = [
            r2.put_object(Bucket='my-bucket', Key=name, Body=content)
            for name, content in files
        ]
        await asyncio.gather(*tasks)

asyncio.run(main())
```

---

## JavaScript/TypeScript (AWS SDK v3)

### 설치

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

### 기본 설정

```typescript
// r2-client.ts
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  ListObjectsV2Command,
  HeadObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const r2 = new S3Client({
  region: "auto",
  endpoint: process.env.R2_ENDPOINT_URL,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY_ID!,
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!,
  },
});

export { r2 };
```

### 유틸리티 클래스

```typescript
// r2-utils.ts
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  ListObjectsV2Command,
  HeadObjectCommand,
  ListObjectsV2CommandOutput,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { Readable } from "stream";

interface R2Object {
  key: string;
  size: number;
  lastModified: Date;
}

class R2Utils {
  private client: S3Client;

  constructor(accountId: string, accessKey: string, secretKey: string) {
    this.client = new S3Client({
      region: "auto",
      endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
      credentials: {
        accessKeyId: accessKey,
        secretAccessKey: secretKey,
      },
    });
  }

  async upload(
    bucket: string,
    key: string,
    body: Buffer | Uint8Array | string | Readable,
    contentType?: string
  ): Promise<void> {
    await this.client.send(
      new PutObjectCommand({
        Bucket: bucket,
        Key: key,
        Body: body,
        ContentType: contentType,
      })
    );
  }

  async download(bucket: string, key: string): Promise<Uint8Array> {
    const response = await this.client.send(
      new GetObjectCommand({
        Bucket: bucket,
        Key: key,
      })
    );

    return response.Body!.transformToByteArray();
  }

  async downloadAsString(bucket: string, key: string): Promise<string> {
    const response = await this.client.send(
      new GetObjectCommand({
        Bucket: bucket,
        Key: key,
      })
    );

    return response.Body!.transformToString();
  }

  async delete(bucket: string, key: string): Promise<void> {
    await this.client.send(
      new DeleteObjectCommand({
        Bucket: bucket,
        Key: key,
      })
    );
  }

  async exists(bucket: string, key: string): Promise<boolean> {
    try {
      await this.client.send(
        new HeadObjectCommand({
          Bucket: bucket,
          Key: key,
        })
      );
      return true;
    } catch {
      return false;
    }
  }

  async *list(
    bucket: string,
    prefix: string = ""
  ): AsyncGenerator<R2Object> {
    let continuationToken: string | undefined;

    do {
      const response: ListObjectsV2CommandOutput = await this.client.send(
        new ListObjectsV2Command({
          Bucket: bucket,
          Prefix: prefix,
          ContinuationToken: continuationToken,
        })
      );

      for (const obj of response.Contents || []) {
        yield {
          key: obj.Key!,
          size: obj.Size!,
          lastModified: obj.LastModified!,
        };
      }

      continuationToken = response.NextContinuationToken;
    } while (continuationToken);
  }

  async getPresignedUrl(
    bucket: string,
    key: string,
    expiresIn: number = 3600
  ): Promise<string> {
    return getSignedUrl(
      this.client,
      new GetObjectCommand({
        Bucket: bucket,
        Key: key,
      }),
      { expiresIn }
    );
  }

  async getPresignedUploadUrl(
    bucket: string,
    key: string,
    contentType: string,
    expiresIn: number = 3600
  ): Promise<string> {
    return getSignedUrl(
      this.client,
      new PutObjectCommand({
        Bucket: bucket,
        Key: key,
        ContentType: contentType,
      }),
      { expiresIn }
    );
  }
}

export { R2Utils };

// 사용 예시
async function main() {
  const r2 = new R2Utils(
    process.env.R2_ACCOUNT_ID!,
    process.env.R2_ACCESS_KEY_ID!,
    process.env.R2_SECRET_ACCESS_KEY!
  );

  // 업로드
  await r2.upload("my-bucket", "test.txt", "Hello R2!");

  // 다운로드
  const content = await r2.downloadAsString("my-bucket", "test.txt");
  console.log(content);

  // 목록 조회
  for await (const obj of r2.list("my-bucket", "images/")) {
    console.log(obj);
  }
}
```

### Express.js 통합

```typescript
// routes/upload.ts
import express from "express";
import multer from "multer";
import { r2 } from "./r2-client";
import { PutObjectCommand } from "@aws-sdk/client-s3";
import { v4 as uuidv4 } from "uuid";

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post("/upload", upload.single("file"), async (req, res) => {
  try {
    const file = req.file;
    if (!file) {
      return res.status(400).json({ error: "No file provided" });
    }

    const key = `uploads/${uuidv4()}-${file.originalname}`;

    await r2.send(
      new PutObjectCommand({
        Bucket: "my-bucket",
        Key: key,
        Body: file.buffer,
        ContentType: file.mimetype,
      })
    );

    res.json({
      success: true,
      key,
      url: `https://cdn.example.com/${key}`,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Upload failed" });
  }
});

export default router;
```

---

## Go (aws-sdk-go-v2)

### 설치

```bash
go get github.com/aws/aws-sdk-go-v2
go get github.com/aws/aws-sdk-go-v2/config
go get github.com/aws/aws-sdk-go-v2/service/s3
go get github.com/aws/aws-sdk-go-v2/credentials
```

### 기본 설정

```go
// r2/client.go
package r2

import (
    "context"
    "fmt"
    "io"
    "os"

    "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/credentials"
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

type Client struct {
    s3Client *s3.Client
}

func NewClient(accountID, accessKey, secretKey string) (*Client, error) {
    r2Resolver := aws.EndpointResolverWithOptionsFunc(
        func(service, region string, options ...interface{}) (aws.Endpoint, error) {
            return aws.Endpoint{
                URL: fmt.Sprintf("https://%s.r2.cloudflarestorage.com", accountID),
            }, nil
        },
    )

    cfg, err := config.LoadDefaultConfig(context.TODO(),
        config.WithEndpointResolverWithOptions(r2Resolver),
        config.WithCredentialsProvider(
            credentials.NewStaticCredentialsProvider(accessKey, secretKey, ""),
        ),
        config.WithRegion("auto"),
    )
    if err != nil {
        return nil, err
    }

    return &Client{
        s3Client: s3.NewFromConfig(cfg),
    }, nil
}

func (c *Client) Upload(ctx context.Context, bucket, key string, body io.Reader, contentType string) error {
    _, err := c.s3Client.PutObject(ctx, &s3.PutObjectInput{
        Bucket:      aws.String(bucket),
        Key:         aws.String(key),
        Body:        body,
        ContentType: aws.String(contentType),
    })
    return err
}

func (c *Client) Download(ctx context.Context, bucket, key string) ([]byte, error) {
    result, err := c.s3Client.GetObject(ctx, &s3.GetObjectInput{
        Bucket: aws.String(bucket),
        Key:    aws.String(key),
    })
    if err != nil {
        return nil, err
    }
    defer result.Body.Close()

    return io.ReadAll(result.Body)
}

func (c *Client) Delete(ctx context.Context, bucket, key string) error {
    _, err := c.s3Client.DeleteObject(ctx, &s3.DeleteObjectInput{
        Bucket: aws.String(bucket),
        Key:    aws.String(key),
    })
    return err
}

// 사용 예시
func main() {
    client, err := NewClient(
        os.Getenv("R2_ACCOUNT_ID"),
        os.Getenv("R2_ACCESS_KEY_ID"),
        os.Getenv("R2_SECRET_ACCESS_KEY"),
    )
    if err != nil {
        panic(err)
    }

    ctx := context.Background()

    // 업로드
    file, _ := os.Open("test.txt")
    defer file.Close()
    client.Upload(ctx, "my-bucket", "test.txt", file, "text/plain")

    // 다운로드
    data, _ := client.Download(ctx, "my-bucket", "test.txt")
    fmt.Println(string(data))
}
```

---

## Java (AWS SDK v2)

### Maven 의존성

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
    <version>2.20.0</version>
</dependency>
```

### 기본 설정

```java
// R2Client.java
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;

import java.net.URI;
import java.nio.file.Path;

public class R2Client {
    private final S3Client s3Client;

    public R2Client(String accountId, String accessKey, String secretKey) {
        this.s3Client = S3Client.builder()
            .endpointOverride(URI.create(
                String.format("https://%s.r2.cloudflarestorage.com", accountId)
            ))
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create(accessKey, secretKey)
            ))
            .region(Region.of("auto"))
            .build();
    }

    public void upload(String bucket, String key, byte[] data, String contentType) {
        s3Client.putObject(
            PutObjectRequest.builder()
                .bucket(bucket)
                .key(key)
                .contentType(contentType)
                .build(),
            RequestBody.fromBytes(data)
        );
    }

    public void uploadFile(String bucket, String key, Path filePath) {
        s3Client.putObject(
            PutObjectRequest.builder()
                .bucket(bucket)
                .key(key)
                .build(),
            filePath
        );
    }

    public byte[] download(String bucket, String key) {
        return s3Client.getObjectAsBytes(
            GetObjectRequest.builder()
                .bucket(bucket)
                .key(key)
                .build()
        ).asByteArray();
    }

    public void delete(String bucket, String key) {
        s3Client.deleteObject(
            DeleteObjectRequest.builder()
                .bucket(bucket)
                .key(key)
                .build()
        );
    }

    public static void main(String[] args) {
        R2Client r2 = new R2Client(
            System.getenv("R2_ACCOUNT_ID"),
            System.getenv("R2_ACCESS_KEY_ID"),
            System.getenv("R2_SECRET_ACCESS_KEY")
        );

        // 업로드
        r2.upload("my-bucket", "test.txt", "Hello R2!".getBytes(), "text/plain");

        // 다운로드
        byte[] data = r2.download("my-bucket", "test.txt");
        System.out.println(new String(data));
    }
}
```

---

## 프레임워크별 통합

### Django

```python
# settings.py
AWS_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'my-bucket'
AWS_S3_ENDPOINT_URL = f"https://{os.environ.get('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
AWS_S3_REGION_NAME = 'auto'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

# django-storages 사용
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### Spring Boot

```yaml
# application.yml
cloud:
  aws:
    s3:
      endpoint: https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com
    credentials:
      access-key: ${R2_ACCESS_KEY_ID}
      secret-key: ${R2_SECRET_ACCESS_KEY}
    region:
      static: auto
```

```java
// S3Config.java
@Configuration
public class S3Config {
    @Value("${R2_ACCOUNT_ID}")
    private String accountId;

    @Value("${R2_ACCESS_KEY_ID}")
    private String accessKey;

    @Value("${R2_SECRET_ACCESS_KEY}")
    private String secretKey;

    @Bean
    public S3Client s3Client() {
        return S3Client.builder()
            .endpointOverride(URI.create(
                String.format("https://%s.r2.cloudflarestorage.com", accountId)
            ))
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create(accessKey, secretKey)
            ))
            .region(Region.of("auto"))
            .build();
    }
}
```

### NestJS

```typescript
// r2.module.ts
import { Module, Global } from "@nestjs/common";
import { S3Client } from "@aws-sdk/client-s3";

@Global()
@Module({
  providers: [
    {
      provide: "R2_CLIENT",
      useFactory: () => {
        return new S3Client({
          region: "auto",
          endpoint: process.env.R2_ENDPOINT_URL,
          credentials: {
            accessKeyId: process.env.R2_ACCESS_KEY_ID!,
            secretAccessKey: process.env.R2_SECRET_ACCESS_KEY!,
          },
        });
      },
    },
  ],
  exports: ["R2_CLIENT"],
})
export class R2Module {}

// r2.service.ts
import { Injectable, Inject } from "@nestjs/common";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

@Injectable()
export class R2Service {
  constructor(@Inject("R2_CLIENT") private readonly r2: S3Client) {}

  async upload(bucket: string, key: string, body: Buffer): Promise<void> {
    await this.r2.send(
      new PutObjectCommand({
        Bucket: bucket,
        Key: key,
        Body: body,
      })
    );
  }
}
```

---

## 다음 단계

- [[../05-projects|실전 프로젝트]] - 완성된 프로젝트 예제
- [[../cheatsheet|치트시트]] - 빠른 참조
