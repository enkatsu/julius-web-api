import pexpect


class JuliusController:
    CONTROL_PATTERNS = ['enter filename->', pexpect.TIMEOUT]
    JULIUS_PARAMS = ['sentence', 'wseq', 'phseq', 'cmscore', 'score']
    JULIUS_PARAMS_PATTERNS = [r'%s\d+:\s+' % param for param in JULIUS_PARAMS]

    def __init__(self, shell_path='/bin/sh', julius_path='julius', input_option='rawfile'):
        self.time_out_seconds = 10
        self.configs = []
        self.julius_path = julius_path
        self.input_option = input_option
        self.julius_process = pexpect.spawn(shell_path)

    def add_config(self, config_path):
        self.configs.append(config_path)

    def create_exec_cmd(self):
        config_option = ' '.join(['-C %s' % config for config in self.configs])
        return '%s %s -input %s' % (self.julius_path, config_option, self.input_option)

    def start(self):
        cmd = self.create_exec_cmd()
        self.julius_process.sendline(cmd)
        index = self.julius_process.expect(JuliusController.CONTROL_PATTERNS, timeout=self.time_out_seconds)
        if index != 0:
            self.end()

    def end(self):
        self.julius_process.close()

    def recognize_file(self, file):
        self.julius_process.sendline(file)
        return self.input_loop([{}])

    def input_loop(self, sentence_list):
        pattern_list = JuliusController.CONTROL_PATTERNS + JuliusController.JULIUS_PARAMS_PATTERNS
        params_start_index = len(JuliusController.CONTROL_PATTERNS)
        index = self.julius_process.expect(pattern_list, timeout=self.time_out_seconds)
        if index == 0:
            sentence_list.pop(-1)
            return sentence_list
        elif index == 1:
            raise TimeoutError()
        else:
            last_index = len(sentence_list) - 1
            param = JuliusController.index2param(index - params_start_index)
            sentence_list[last_index][param] = self.julius_process.readline().decode('utf-8')
            if index == len(pattern_list) - 1:
                sentence_list.append({})
            return self.input_loop(sentence_list)

    @staticmethod
    def index2param(index):
        return JuliusController.JULIUS_PARAMS[index]
