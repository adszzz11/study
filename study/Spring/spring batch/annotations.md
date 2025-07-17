
@BeforeJob
- 호출 조건: Job이 시작되기 전에 항상 호출됩니다.
- 에러 발생 시: JobExecution에 실패 상태가 기록되며, Job이 중단될 수 있습니다.
	@BeforeStep
	- 호출 조건: 각 Step이 실행되기 전에 항상 호출됩니다.
    - 에러 발생 시: StepExecution에 실패 상태가 기록되며, 해당 Step의 실행이 중단될 수 있습니다.
      @BeforeChunk
	    - 호출 조건: Chunk 단위 작업이 시작되기 전에 항상 호출됩니다.
		- 에러 발생 시: ChunkExecution에 실패 상태가 기록되며, 해당 Chunk의 실행이 중단될 수 있습니다.
            --------
            Read 관련 애노테이션
            @BeforeRead
            - 호출 조건: `ItemReader`에서 데이터를 읽기 전에 항상 호출됩니다.
			- 에러 발생 시: 항목 읽기가 중단되며, Chunk의 실패로 이어질 수 있습니다.
            @OnSkipInRead  (ItemReader에서 오류가 발생해 항목이 스킵될 때)
			- 호출 조건: `ItemReader`에서 오류가 발생해 항목이 스킵될 때 호출됩니다.
			- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Chunk 실패로 이어질 수 있습니다.
			@OnReadError  (ItemReader에서 오류가 발생했을 때)
			- 호출 조건: `ItemReader`에서 오류가 발생했을 때 호출됩니다.
			- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Chunk 실패로 이어질 수 있습니다.
			@AfterRead  (ItemReader에서 항목을 성공적으로 읽어왔을 때)
			- 호출 조건: `ItemReader`에서 항목을 성공적으로 읽어온 후 호출됩니다.
			- 에러 발생 시: ChunkExecution에 실패 상태가 기록되지만, 이미 읽어진 데이터는 처리됩니다.
            --------
			Process 관련 애노테이션
            @BeforeProcess
			- 호출 조건: `ItemProcessor`에서 데이터를 처리하기 전에 항상 호출됩니다.
			- 에러 발생 시: 항목 처리가 중단되며, Chunk의 실패로 이어질 수 있습니다.
			@OnProcessError  (ItemProcessor에서 오류가 발생했을 때)
			- 호출 조건: `ItemProcessor`에서 오류가 발생했을 때 호출됩니다.
			- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Chunk 실패로 이어질 수 있습니다.
            @OnSkipInProcess  (ItemProcessor에서 오류가 발생해 항목이 스킵될 때)
			- 호출 조건: `ItemProcessor`에서 오류가 발생해 항목이 스킵될 때 호출됩니다.
			- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Chunk 실패로 이어질 수 있습니다.
			@AfterProcess  (ItemProcessor에서 항목을 성공적으로 처리했을 때)
			- 호출 조건: `ItemProcessor`에서 항목을 성공적으로 처리한 후 호출됩니다.
			- 에러 발생 시: ChunkExecution에 실패 상태가 기록되지만, 이미 처리된 데이터는 영향을 받지 않습니다.
            --------
            Write 관련 애노테이션
            @BeforeWrite
			- 호출 조건: `ItemWriter`에서 데이터를 쓰기 전에 항상 호출됩니다.
			- 에러 발생 시: 항목 쓰기가 중단되며, Chunk의 실패로 이어질 수 있습니다.
            @OnSkipInWrite  (ItemWriter에서 오류가 발생해 항목이 스킵될 때)
			- 호출 조건: `ItemWriter`에서 오류가 발생해 항목이 스킵될 때 호출됩니다.
			- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Chunk 실패로 이어질 수 있습니다.
            @OnWriteError  (ItemWriter에서 오류가 발생했을 때)
			- 호출 조건: `ItemWriter`에서 오류가 발생했을 때 호출됩니다.
			- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Chunk 실패로 이어질 수 있습니다.
            @AfterWrite  (ItemWriter에서 항목을 성공적으로 썼을 때)
			- 호출 조건: `ItemWriter`에서 항목을 성공적으로 쓴 후 호출됩니다.
			- 에러 발생 시: ChunkExecution에 실패 상태가 기록되지만, 이미 쓰여진 데이터는 그대로 유지됩니다.
            --------
        @AfterChunk  (Chunk가 성공적으로 완료되었을 때)
		- 호출 조건: Chunk 단위 작업이 성공적으로 완료된 후 호출됩니다.
		- 에러 발생 시: ChunkExecution에 실패 상태가 기록되지만, Chunk는 이미 성공적으로 완료된 상태입니다.
        @AfterChunkError  (Chunk 처리 중 오류가 발생했을 때)
		- 호출 조건: Chunk 처리 중 오류가 발생했을 때 호출됩니다.
		- 에러 발생 시: 추가적인 오류가 ChunkExecution에 기록되며, Step이나 Job의 상태를 악화시킬 수 있습니다.
    @AfterStep
	- 호출 조건: 각 Step이 완료된 후에 항상 호출됩니다.
	- 에러 발생 시: StepExecution에 오류가 기록되지만, Step 자체는 이미 완료된 상태입니다.
@AfterJob
- 호출 조건: Job이 완료된 후에 항상 호출됩니다.
- 에러 발생 시: JobExecution에 실패 상태가 기록되며, Job이 중단될 수 있습니다.