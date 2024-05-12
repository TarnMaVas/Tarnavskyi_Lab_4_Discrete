'''
Module containing an implementation of a finite state machine
that represents my daily routine.
'''

import random

RESTING_PHRASES = [
    "Baldur's Gate 3 is such a good game!",
    "Music is so relaxing...",
    "Terry Pratchett really is the best fiction writer. What a great book!",
    "Doing Math Analysis also counts as resting, right?"
]

class FSM:
    '''
    Class representing a finite state machine.
    '''
    def __init__(self):
        '''
        Constructor of the FSM class.
        Sets up the states and chooses the initial one.
        '''
        self.SLEEP = self.__setup_sleep()
        next(self.SLEEP)
        self.EAT = self.__setup_eat()
        next(self.EAT)
        self.STUDY = self.__setup_study()
        next(self.STUDY)
        self.DO_CHORES = self.__setup_do_chores()
        next(self.DO_CHORES)
        self.REST = self.__setup_rest()
        next(self.REST)

        self.cur_state = self.SLEEP

        self._energy = 100
        self._hunger_level = 0


    @property
    def energy(self)-> int:
        '''
        Property that represents my energy level.
        '''
        return self._energy


    @energy.setter
    def energy(self, value: int):
        '''
        Setter for the energy level.
        '''
        self._energy = min(100, max(0, value))


    @property
    def hunger_modifier(self)-> int:
        '''
        Property that represents the how
        my hunger influences my energy.
        '''
        return 2 if self._hunger_level > 25 else 1


    def accept(self, hour: int):
        '''
        Accepts the given hour and changes the state of the FSM accordingly.
        '''
        self.cur_state.send(hour)


    def __setup_sleep(self):
        '''
        Function that represents the SLEEP state.
        It represents any time when I'm sleeping.
        '''
        while True:

            hour = yield

            if hour is None:
                return 

            self.energy += random.randint(5, 10)
            self._hunger_level += random.randint(1, 7)

            if 0 <= hour < 7:

                if random.random() <= 0.1:

                    cool_print(hour, "Ugh, another air alarm tonight... Guess I have to go to the shelter now.")
                    self.drowsy = True
                    self.cur_state = self.DO_CHORES

                else:

                    cool_print(hour, 'Zzz...')

            elif hour == 7:

                if random.random() <= 0.33:

                    cool_print(hour, 'Gosh, I feel horrible. Was I sleeping or was someone beating me up?')
                    self.energy -= 30

                else:

                    cool_print(hour, 'Rise and shine!')

                self.cur_state = self.EAT

            elif self._hunger_level > 40:

                cool_print(hour, "What a nice nap! Now I'm hungry though...")
                self.cur_state = self.EAT

            else:

                if hour == 19:
                        
                    cool_print(hour, "That was a good nap. Time to supper now.")
                    self.cur_state = self.EAT

                else:

                    cool_print(hour, "Well, that was a good snooze. Let's get back to work!")
                    self.cur_state = random.choice([self.DO_CHORES, self.STUDY])


    def __setup_eat(self):
        '''
        Function that represents the EAT state.
        It represents any time when I'm eating.
        '''
        while True:

            hour = yield

            if hour is None:
                return 

            self._hunger_level = 0

            if hour == 8:

                cool_print(hour, "That was some delicious breakfast! Time to work now...")
                self.cur_state = random.choice([self.STUDY, self.DO_CHORES])

            elif hour == 20 and self._hunger_level >= 8:

                cool_print(hour, 'What a nice supper!')
                self.cur_state = random.choice([self.REST, self.STUDY])


            elif self.energy < 10:

                cool_print(hour, "That sure was tasty, but I'm still very tired. Time for some sleep.")
                self.cur_state = self.SLEEP

            else:

                cool_print(hour, "That was delicious! Let's get back to work.")
                self.cur_state = random.choice([self.STUDY, self.DO_CHORES])


    def __setup_rest(self):
        '''
        Function that represents the REST state.
        It represents any time when I'm resting.
        '''
        while True:

            hour = yield

            if hour is None:
                return 

            self.energy += random.randint(1, 5)
            self._hunger_level += random.randint(1, 7)

            if self._hunger_level > 40:

                cool_print(hour, "I'm feeling pretty hungry. Let's eat something.")
                self.cur_state = self.EAT

            elif hour == 0:

                if self.energy > 50:

                    cool_print(hour, random.choice(RESTING_PHRASES))

                else:

                    cool_print(hour, random.choice(RESTING_PHRASES) + " I'm tired though. Time to sleep.")
                    self.cur_state = self.SLEEP

            elif hour == 1:

                cool_print(hour, 'Whoops, I had so much fun, it seems I forgot about time! I should really go to sleep now.')

            elif hour == 19 and self._hunger_level >= 8:

                cool_print(hour, random.choice(RESTING_PHRASES) + " It's time for supper now.")

            else:

                if random.random() <= 0.7:

                    cool_print(hour, random.choice(RESTING_PHRASES) + " Let's get back to work!")
                    self.cur_state = random.choice([self.STUDY, self.DO_CHORES])

                else:

                    cool_print(random.choice(RESTING_PHRASES))


    def __setup_study(self):
        '''
        Function that represents the STUDY state.
        It represents any time when I'm studying.
        '''
        while True:

            hour = yield

            if hour is None:
                return 

            self.energy -= random.randint(5, 10) * self.hunger_modifier
            self._hunger_level += random.randint(1, 7)

            if self._hunger_level > 40:

                cool_print(hour, "What a productive day. Although I'm very hungry now, let's eat something, shall we?")
                self.cur_state = self.EAT
            
            elif hour == 19 and self._hunger_level >= 8:

                cool_print(hour, "That was some good studying! Time to supper.")
                self.cur_state = self.EAT

            elif hour == 0:

                cool_print(hour, "Whew, it's so late already! I'm going to bed now.")
                self.cur_state = self.SLEEP

            elif self.energy < 10:

                cool_print(hour, "I've been studying for so long and I'm so tired... Guess I'll take a nap.")
                self.cur_state = self.SLEEP

            else:

                if random.random() <= 0.7:

                    cool_print(hour, "Studying is fun. Let's keep going.")

                else:

                    cool_print(hour, "That was some good studying! Time to rest now.")
                    self.cur_state = self.REST


    def __setup_do_chores(self):
        '''
        Function that represents the DO_CHORES state.
        It represents any time when I'm doing things that
        I don't really wan't to, but have to do, like going
        to shelter during air alarm.
        '''
        while True:

            hour = yield

            if hour is None:
                return 

            self.energy -= random.randint(5, 10) * self.hunger_modifier
            self._hunger_level += random.randint(1, 7)

            if self._hunger_level > 40:

                cool_print(hour, "Ugh, that's enough of these chores. All the work made me hungry too, let's eat something.")
                self.cur_state = self.EAT

            elif hour == 19 and self._hunger_level >= 8:

                cool_print(hour, "That's enough chores for now. Let's have some supper.")
                self.cur_state = self.EAT

            elif hour == 7:

                cool_print(hour, "Just great. Seems like I don't have the time to go back to sleep anymore. Well, let's at least eat something.")
                self.cur_state = self.EAT

            elif hour < 7:

                if random.random() <= 0.7:

                    cool_print(hour, 'Thank God it ended quickly. I can go back to sleep now.')
                    self.cur_state = self.SLEEP

                else:

                    cool_print(hour, 'I really hope this air alarm will be over soon...')

            elif self.energy < 10:

                cool_print(hour, "I've been working for so long and I'm so tired... Guess I'll take a nap.")
                self.cur_state = self.SLEEP

            else:

                if random.random() <= 0.33:

                    cool_print(hour, 'Finally, I finished all the tedious work. Time to rest now.')
                    self.cur_state = self.REST

                else:
                    cool_print(hour, 'Still working...')


def cool_print(hour: int, message: str):
    '''
    Function that prints the given message with a cool
    time prefix.
    '''
    print(f'{hour:02}:00 - {message}')


def day_simulation(days: int = 1):
    '''
    Function that simulates a given number of my days.
    '''
    fsm = FSM()

    for hour in list(range(24)) * days:

        fsm.accept(hour)
