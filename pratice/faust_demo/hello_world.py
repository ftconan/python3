"""
# @author: magician
# @file:   hello_world.py
# @date:   2022/1/11
"""
import faust

app = faust.App(
    'hello-world',
    broker='kafka://localhost:9092',
    producer_api_version='0.10.2',
    store='rocksdb://',
)

greetings_topic = app.topic('greetings', key_type=str, value_type=str)


@app.agent(greetings_topic)
async def print_greetings(stream):
    async for values in stream.clone().take(10, within=3):
        print(f'stream len: {len(values)}')
        async for key, value in stream.items():
            print(key, value)


@app.task
async def produce():
    for i in range(100):
        await print_greetings.send(key='greetings', value=f'hello {i}')


if __name__ == '__main__':
    app.main()
