# Julius Web API Server

## Installation

```bash
curl -o dictation-kit-v4.4.zip https://jaist.dl.osdn.jp/julius/66544/dictation-kit-v4.4.zip && \
unzip dictation-kit-v4.4.zip && \
mv dictation-kit-v4.4 julius/kit/dictation-kit-v4.4 && \
rm dictation-kit-v4.4.zip

pip install -r requirements.txt
```

### Julius speech recognition packages

- https://jaist.dl.osdn.jp/julius/66544/dictation-kit-v4.4.zip
- https://jaist.dl.osdn.jp/julius/68910/lsr-kit-v4.4.2.1a.zip
- http://iij.dl.osdn.jp/julius/68910/ssr-kit-v4.4.2.1a.zip 

## Usage

### Web server

```bash
python main.py
```

http://localhost:8888

### JuliusController

```python
from julius_controller import JuliusController

# initialize JuliusController

shell_path = '/path/to/shell'
julius_path = '/path/to/julius'
julius_controller = JuliusController(shell_path=shell_path, julius_path=julius_path)
config_path = '/path/to/jconf'
julius_controller.add_config(config_path)

# start Julius process

julius_controller.start()

# recognize file

wav_file_path = '/path/to/wav_file'
result = julius_controller.recognize_file(wav_file_path)
print(result)
# [{
# 	"sentence": "これ は マイク の テスト です 。\r\n",
# 	"wseq": "<s> これ+代名詞 は+助詞 マイク+名詞 の+助詞 テスト+名詞 です+助動詞 </s>\r\n",
# 	"phseq": "silB | k o r e | w a | m a i k u | n o | t e s u t o | d e s u | silE\r\n",
# 	"cmscore": "0.517 0.687 0.481 0.570 0.3260.165039\r\n"
# }]

# close Julius process
julius_controller.end()
```

### Run tests

```bash
python -m unittest discover tests
```
