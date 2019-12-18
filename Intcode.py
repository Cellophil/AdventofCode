import numpy as np
input = []
# from numba import jitclass

# @jitclass
class intcomputer():

    def __init__(self,input0,FLAGS=[],BASE=0,extramemory=100000):
        
        input0 = [np.int64(s) for s in input0.split(',')]
        self.program0 = np.append(input0,np.zeros(np.int64(extramemory),dtype=np.int64))
        self.reset()

    def reset(self):
        self.pos = 0
        self.program = self.program0.copy()
        self.ACTIVE = True
        self.BASE = 0
        self.REQUIRE_INPUT = False
        self.OUTPUT_AVAILABLE = False
        self.input = []
        self.output = []

    def get_opcode_and_index(self):
        s = str(self.program[self.pos])
        for l in range(5-len(s)):
            s = '0'+s
        
        opcode = np.int(s[3:5])
        mod1 = np.int(s[2])
        mod2 = np.int(s[1])
        mod3 = np.int(s[0])

        index1 = np.nan
        index2 = np.nan
        index3 = np.nan

        if mod1==1:
            index1 = self.pos+1
        elif mod1==2:
            index1 = self.BASE+self.program[self.pos+1]
        else:
            index1 = self.program[self.pos+1]

        if opcode in [1,2,5,6,7,8]:
            if mod2==1:
                index2 = self.pos+2
            elif mod2==2:
                index2 = self.BASE+self.program[self.pos+2]
            else:
                index2 = self.program[self.pos+2]

        if opcode in [1,2,7,8]:
            if mod3==1:
                index3 = self.pos+3
            elif mod3==2:
                index3 = self.BASE+self.program[self.pos+3]
            else:
                index3 = self.program[self.pos+3]

        return [opcode, index1, index2, index3]

    def step_until(self):
        n = 0
        while len(self.output)==0:
            n+=1
            if not self.ACTIVE:
                return 'program terminated'
            self.step()
            if self.REQUIRE_INPUT:
                return 'require input'
            if n>100000:
                raise Exception('100000 steps, no output/input/end... fishy')

        if self.output[0] == '99':
            return 'program terminated'
        else:
            return 'there is output'

    def put_input(self,x):
        self.input.append(x)
        return

    def get_output(self):
        if self.ACTIVE == False:
            return 'program terminated'
        if len(self.output) == 0:
             return 'There is no further output.'
        else:
            o = self.output.pop(0)
            if len(self.output) == 0:
                self.OUTPUT_AVAILABLE = False
            return o

    def _get_input(self):
        if len(self.input)==0:
            self.REQUIRE_INPUT = True
            return False
        else:
            self.REQUIRE_INPUT = False
            i = self.input.pop(0)
            return i

    def _get_input(self):
        if len(self.input)==0:
            self.REQUIRE_INPUT = True
            return [False,-1]
        else:
            self.REQUIRE_INPUT = False
            i = self.input.pop(0)
            return [True,i]

    def _put_output(self,x):
        self.output.append(x)
        self.OUTPUT_AVAILABLE = True
        return

    def _check_input_block(self):
        if self.REQUIRE_INPUT:
            if len(self.input) == 0:
                raise Exception('Please provide input!')

    def step(self):
        self._check_input_block()
        if not self.ACTIVE:
            return
        [opcode, index1, index2, index3] = self.get_opcode_and_index()

        if opcode == 1:
            self.program[index3] = self.program[index2] + self.program[index1]
            self.pos += 4
        elif opcode == 2:
            self.program[index3] = self.program[index2] * self.program[index1]
            self.pos += 4
        elif opcode == 3:
            i = self._get_input()
            if i[0]:
                self.program[index1] = i[1]
                self.pos += 2
            else:
                self.REQUIRE_INPUT=True
        elif opcode == 4:
            self._put_output(self.program[index1])
            self.pos += 2
        elif opcode == 5:
            if self.program[index1]:
                self.pos = self.program[index2]
            else:
                self.pos += 3
        elif opcode == 6:
            if not self.program[index1]:
                self.pos = self.program[index2]
            else:
                self.pos += 3
        elif opcode == 7:
            if self.program[index1] < self.program[index2]:
                self.program[index3] = 1
            else:
                self.program[index3] = 0
            self.pos += 4
        elif opcode == 8:
            if self.program[index1] == self.program[index2]:
                self.program[index3] = 1
            else:
                self.program[index3] = 0
            self.pos += 4
        elif opcode == 9:
            self.BASE += self.program[index1]
            self.pos += 2
        elif opcode == 99:
            self.ACTIVE = False
            self.pos = -1
        else:
            raise Exception('Opcode error: ',[pos,opcode])
        return


if __name__ == '__main__':
    testprogram = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,0,1020,1101,0,23,1010,1102,1,31,1009,1101,34,0,1019,1102,38,1,1004,1101,29,0,1017,1102,1,25,1018,1102,20,1,1005,1102,1,24,1008,1101,897,0,1024,1101,0,28,1016,1101,1,0,1021,1101,0,879,1028,1102,1,35,1012,1101,0,36,1015,1101,311,0,1026,1102,1,37,1011,1101,26,0,1014,1101,21,0,1006,1102,1,32,1002,1102,1,33,1003,1102,27,1,1001,1102,1,667,1022,1101,0,892,1025,1101,664,0,1023,1101,30,0,1000,1101,304,0,1027,1101,22,0,1013,1102,1,874,1029,1102,1,39,1007,109,12,21108,40,41,1,1005,1013,201,1001,64,1,64,1106,0,203,4,187,1002,64,2,64,109,5,1205,4,221,4,209,1001,64,1,64,1106,0,221,1002,64,2,64,109,5,21108,41,41,-5,1005,1017,243,4,227,1001,64,1,64,1106,0,243,1002,64,2,64,109,-30,2101,0,8,63,1008,63,30,63,1005,63,269,4,249,1001,64,1,64,1105,1,269,1002,64,2,64,109,15,2101,0,-5,63,1008,63,35,63,1005,63,293,1001,64,1,64,1106,0,295,4,275,1002,64,2,64,109,28,2106,0,-8,1001,64,1,64,1105,1,313,4,301,1002,64,2,64,109,-22,1205,7,329,1001,64,1,64,1106,0,331,4,319,1002,64,2,64,109,-12,1208,6,37,63,1005,63,351,1001,64,1,64,1106,0,353,4,337,1002,64,2,64,109,-3,2108,21,8,63,1005,63,375,4,359,1001,64,1,64,1106,0,375,1002,64,2,64,109,14,1201,-5,0,63,1008,63,39,63,1005,63,401,4,381,1001,64,1,64,1105,1,401,1002,64,2,64,109,17,1206,-9,419,4,407,1001,64,1,64,1105,1,419,1002,64,2,64,109,-10,21101,42,0,-4,1008,1015,42,63,1005,63,445,4,425,1001,64,1,64,1105,1,445,1002,64,2,64,109,-5,1206,7,457,1105,1,463,4,451,1001,64,1,64,1002,64,2,64,109,-6,2107,34,-5,63,1005,63,479,1105,1,485,4,469,1001,64,1,64,1002,64,2,64,109,-8,2102,1,5,63,1008,63,23,63,1005,63,505,1106,0,511,4,491,1001,64,1,64,1002,64,2,64,109,5,2102,1,1,63,1008,63,21,63,1005,63,537,4,517,1001,64,1,64,1105,1,537,1002,64,2,64,109,15,21107,43,44,-6,1005,1014,555,4,543,1106,0,559,1001,64,1,64,1002,64,2,64,109,-6,1207,-7,38,63,1005,63,579,1001,64,1,64,1106,0,581,4,565,1002,64,2,64,109,-17,1201,4,0,63,1008,63,28,63,1005,63,601,1106,0,607,4,587,1001,64,1,64,1002,64,2,64,109,14,2107,31,-9,63,1005,63,625,4,613,1105,1,629,1001,64,1,64,1002,64,2,64,109,15,21102,44,1,-7,1008,1019,44,63,1005,63,651,4,635,1106,0,655,1001,64,1,64,1002,64,2,64,109,3,2105,1,-6,1106,0,673,4,661,1001,64,1,64,1002,64,2,64,109,-14,21101,45,0,2,1008,1017,42,63,1005,63,693,1105,1,699,4,679,1001,64,1,64,1002,64,2,64,109,5,21107,46,45,-8,1005,1012,719,1001,64,1,64,1105,1,721,4,705,1002,64,2,64,109,-19,2108,21,7,63,1005,63,737,1106,0,743,4,727,1001,64,1,64,1002,64,2,64,109,9,1207,-2,25,63,1005,63,761,4,749,1106,0,765,1001,64,1,64,1002,64,2,64,109,-10,1208,1,27,63,1005,63,783,4,771,1106,0,787,1001,64,1,64,1002,64,2,64,109,5,1202,4,1,63,1008,63,29,63,1005,63,807,1106,0,813,4,793,1001,64,1,64,1002,64,2,64,109,8,21102,47,1,0,1008,1013,50,63,1005,63,833,1106,0,839,4,819,1001,64,1,64,1002,64,2,64,109,-12,1202,8,1,63,1008,63,31,63,1005,63,865,4,845,1001,64,1,64,1105,1,865,1002,64,2,64,109,34,2106,0,-7,4,871,1105,1,883,1001,64,1,64,1002,64,2,64,109,-18,2105,1,7,4,889,1105,1,901,1001,64,1,64,4,64,99,21101,0,27,1,21101,915,0,0,1106,0,922,21201,1,13801,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1106,0,922,21201,1,0,-1,21201,-2,-3,1,21102,957,1,0,1105,1,922,22201,1,-1,-2,1106,0,968,21202,-2,1,-2,109,-3,2106,0,0]

    c = intcomputer(testprogram)
    c.put_input(1)

    while (c.ACTIVE == True):
        c.step_until()

        print(c.get_output())
