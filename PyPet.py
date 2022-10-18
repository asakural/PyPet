from pickle import FALSE
import time
import random
import os

def clearScreen():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # checks if you're using windows
        command = 'cls'
    os.system(command)

playing = True #controls the entire game loop
dead = False #controls the main gameplay loop
slept_recently = False #used to prevent stat drain when pet wakes up
elder_death = False #used to provide a special message for natural death
guesses = 0 #used to score one of the games

from pet_sprites import other_pet, baby_pet, child_pet, teen_pet, adult_pet

class pypet: #This class contains all of the pet's stats and many of the methods related to managing them
    
    life_stage = "baby"
    hunger_need = 100
    fun_need = 100
    health_need = 100
    clean_need = 100
    sleep_need = 100
    age = 0
    personality = 'normal'
    d = 5 #used to determine 'days until birthday'
    
    #initialization
    def __init__(self, name):
        self.name = name
    
    #This simply displays your pet's stats and caps them at 100
    def print_stats(self):
        if (self.hunger_need >= 100):
            self.hunger_need = 100
            print("Hunger: ".ljust(10,' ')+str(self.hunger_need))
        elif (self.hunger_need < 0):
            self.hunger_need = 0
            print("Hunger: ".ljust(10,' ')+str(self.hunger_need))
        else:   
            print("Hunger: ".ljust(10,' ')+str(self.hunger_need))
        
        if (self.fun_need >= 100):
            self.fun_need = 100
            print("Fun: ".ljust(10,' ')+str(self.fun_need))
        elif (self.fun_need < 0):
            self.fun_need = 0
            print("Fun: ".ljust(10,' ')+str(self.fun_need))
        else:
            print("Fun: ".ljust(10,' ')+str(self.fun_need))
        
        if (self.clean_need < 0):
            self.clean_need = 0
            print("Hygiene: ".ljust(10,' ')+str(self.clean_need))
        else:
            print("Hygiene: ".ljust(10,' ')+str(self.clean_need))

        if (self.sleep_need >= 100):
            self.sleep_need = 100
            print("Sleep: ".ljust(10,' ')+str(self.sleep_need))
        elif (self.sleep_need < 0):
            self.sleep_need = 0
            print("Health: ".ljust(10,' ')+str(self.sleep_need))
        else:
            print("Sleep: ".ljust(10,' ')+str(self.sleep_need))
        
        if (self.health_need >= 100):
            self.health_need = 100
            print("Health: ".ljust(10,' ')+str(self.health_need))
        elif (self.health_need < 0):
            self.health_need = 0
            print("Health: ".ljust(10,' ')+str(self.health_need))
        else:
            print("Health: ".ljust(10,' ')+str(self.health_need))

    #This is what causes your pet's stats to drain
    def need_decay(self):
        
        if (self.life_stage == "baby"):
            if (self.hunger_need > 0):
                self.hunger_need -= 6

            if (self.fun_need > 0):
                self.fun_need -= 10

            if (self.clean_need > 0):
                self.clean_need -= 10
            
            if (slept_recently == False):
                if (self.sleep_need > 0):
                    self.sleep_need -= 10
            else:
                slept_recently == False
                pass

            if (self.fun_need < 25):
                self.hunger_need -= 1
                self.clean_need -= 1
                self.sleep_need -= 1

            if (self.health_need > 60):
                if (self.hunger_need <= 40 or self.clean_need <= 40):
                    self.health_need -= 2

                elif (self.hunger_need < 40 and self.clean_need < 40):
                    self.health_need -= 4

            elif (self.health_need <= 60):
                if (self.hunger_need >= 40 and self.clean_need >= 40):
                    self.health_need -= 1
                elif (self.hunger_need < 40 or self.clean_need < 40):
                    self.health_need -= 2

        elif (self.age == 5 or self.age == 15 or self.age == 25): #traits don't take effect on the pet's birthday; all pets are treated as 'normal' until the day after
            if (self.hunger_need > 0):
                if (self.life_stage == "child"):
                    self.hunger_need -= 4
                else:
                    self.hunger_need -= 3

            if (self.fun_need > 0):
                if (self.life_stage == "child"):
                    self.fun_need -= 8
                elif (self.life_stage == "teen"):
                    self.fun_need -= 5
                else:
                    self.fun_need -= 3

            if (self.clean_need > 0):
                if (self.life_stage == "child" or self.life_stage == "elder"):
                    self.clean_need -= 8
                else:
                    self.clean_need -= 5

            if (slept_recently == False):
                    if (self.life_stage == "child" or self.life_stage == "elder"):
                        self.sleep_need -= 8
                    else:
                        self.sleep_need -= 5
            else:
                slept_recently == False
                pass

            if (self.fun_need < 25):
                    self.hunger_need -= 2
                    self.clean_need -= 2
                    self.sleep_need -= 2

            if (self.health_need > 60):
                if (self.hunger_need <= 40 or self.clean_need <= 40):
                    self.health_need -= 2

                elif (self.hunger_need < 40 and self.clean_need < 40):
                    self.health_need -= 4

                elif (self.health_need <= 60):
                    if (self.hunger_need >= 40 and self.clean_need >= 40):
                        self.health_need -= 1
                    elif (self.hunger_need < 40 or self.clean_need < 40):
                        self.health_need -= 2

                if (self.life_stage == "elder"):
                    self.health_need -= 1
                else: 
                    pass

        else:
            if (self.hunger_need > 0):
                if (self.life_stage == "child"):
                    self.hunger_need -= 4
                else:
                    self.hunger_need -= 3

            if (self.fun_need > 0):
                if (self.personality == "restless"):
                    if (self.life_stage == "child"):
                        self.fun_need -= 10
                    elif (self.life_stage == "teen"):
                        self.fun_need -= 7
                    else:
                        self.fun_need -= 5
                elif (self.personality == "carefree" or self.personality == "balanced"):
                    if (self.life_stage == "child"):
                        self.fun_need -= 6
                    elif (self.life_stage == "teen"):
                        self.fun_need -= 3
                    else:
                        self.fun_need -= 2
                else:
                    if (self.life_stage == "child"):
                        self.fun_need -= 8
                    elif (self.life_stage == "teen"):
                        self.fun_need -= 5
                    else:
                        self.fun_need -= 3

            if (self.clean_need > 0):
                if (self.personality == "messy"):
                    if (self.life_stage == "child" or self.life_stage == "elder"):
                        self.clean_need -= 10
                    else:
                        self.clean_need -= 7
                elif (self.personality == "neat" or self.personality == "balanced"):
                    if (self.life_stage == "child" or self.life_stage == "elder"):
                        self.clean_need -= 6
                    else:
                        self.clean_need -= 3
                else:
                    if (self.life_stage == "child" or self.life_stage == "elder"):
                        self.clean_need -= 8
                    else:
                        self.clean_need -= 5

            if (slept_recently == False):
                if (self.life_stage == "child" or self.life_stage == "elder"):
                    self.sleep_need -= 8
                else:
                    self.sleep_need -= 5
            else:
                slept_recently == False

            if (self.fun_need < 25):
                    self.hunger_need -= 2
                    self.clean_need -= 2
                    self.sleep_need -= 2

            if (self.health_need > 60):
                if (self.personality == "sickly"):
                    if (self.hunger_need <= 45 or self.clean_need <= 45):
                        self.health_need -= 2

                    elif (self.hunger_need < 45 and self.clean_need < 45):
                        self.health_need -= 4

                    elif (self.health_need <= 65):
                        if (self.hunger_need >= 45 and self.clean_need >= 45):
                            self.health_need -= 1
                        elif (self.hunger_need < 45 or self.clean_need < 45):
                            self.health_need -= 2
                    
                    if (self.life_stage == "elder"):
                        self.health_need -= 2
                    else: 
                        pass

                else:
                    if (self.hunger_need <= 40 or self.clean_need <= 40):
                        self.health_need -= 2

                    elif (self.hunger_need < 40 and self.clean_need < 40):
                        self.health_need -= 4

                    elif (self.health_need <= 60):
                        if (self.hunger_need >= 40 and self.clean_need >= 40):
                            self.health_need -= 1
                        elif (self.hunger_need < 40 or self.clean_need < 40):
                            self.health_need -= 2

                    if (self.life_stage == "elder"):
                        self.health_need -= 1
                    else: 
                        pass
        
    #This also allows stats to drain, but this variation is only used while a pet is asleep
    def need_decay_sleep(self):
        
        self.age += 1
        
        if (self.age == "baby"):
            if (self.hunger_need > 0):
                self.hunger_need -= 5

            if (self.clean_need > 0):
                self.clean_need -= 10

        else:
            if (self.personality == "greedy"):
                if (self.life_stage == "child"):
                    self.hunger_need -= 3
                else:
                    self.hunger_need -= 2
            elif (self.personality == "balanced"):
                pass
            else:
                if (self.life_stage == "child"):
                    self.hunger_need -= 2
                else:
                    self.hunger_need -= 1

            if (self.personality == "messy"): 
                if (self.clean_need > 0):
                    if (self.life_stage == "child"):
                        self.clean_need -= 7
                    else:
                        self.clean_need -= 4
                    
            elif (self.personality == "neat" or self.personality == "balanced"):
                if (self.clean_need > 0):
                    if (self.life_stage == "child"):
                        self.clean_need -= 3
                    else:
                        self.clean_need -= 1
            else:
                if (self.clean_need > 0):
                    if (self.life_stage == "child"):
                        self.clean_need -= 5
                    else:
                        self.clean_need -= 2
        
    #This lets you feed your pet and restore their hunger need
    def feed(self):
        print()
        if (self.hunger_need >= 80):
            print(self.name,"isn't hungry right now!")
            time.sleep(2)
            print()
        else:
            clearScreen()
            if (self.life_stage == "baby"):
                print(baby_pet[1])
            elif (self.life_stage == "child"):
                print(child_pet[1])
            elif (self.life_stage == "teen"):
                print(teen_pet[1])
            else:
                print(adult_pet[1])
            print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
            print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
            pet.birthday()
            print()
            pet.print_stats()
            print()
            self.hunger_need += 40
            print("Feeding",self.name+"...")
            time.sleep(2)
            print()
    
    #This lets you bathe your pet and restore their hygiene need
    def clean(self):
        print()
        clearScreen()
        if (self.life_stage == "baby"):
            print(baby_pet[3])
        elif (self.life_stage == "child"):
            print(child_pet[3])
        elif (self.life_stage == "teen"):
            print(teen_pet[3])
        else:
            print(adult_pet[3])
        print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
        print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
        pet.birthday()
        print()
        pet.print_stats()
        print()
        
        self.clean_need = 100
        print("Giving",self.name,"a bath...")
        time.sleep(2)
        print()
    
    #This lets you play with your pet and restore their fun need
    def play(self):
        print()
        clearScreen()
        if (self.life_stage == "baby"):
            print(baby_pet[2])
        elif (self.life_stage == "child"):
            print(child_pet[2])
        elif (self.life_stage == "teen"):
            print(teen_pet[2])
        else:
            print(adult_pet[2])
        print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
        print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
        pet.birthday()
        print()
        pet.print_stats()
        print()
        
        time.sleep(1)

        while True:
            play = str(input("Would you like to play a game (more fun) or give your pet a toy (less fun)? Type 'g' for game or 't' for toy."))

            if (play == 'g'):
                number_game()

                if (guesses < 5):
                    self.fun_need += 80
                else:
                    self.fun_need += 70
                break

            elif (play == 't'):
                print(self.name, "plays with a toy.")
                self.fun_need += 40
                break

            else:
                print("Sorry, I didn't get that.")
                continue

        time.sleep(2)
        print()
     
   #This send your pet to bed and restores their sleep need 
    def sleep(self):
        print()
        if (self.sleep_need > 75):
            print(self.name,"isn't sleepy right now!")
            time.sleep(2)
            print()
        else:
            clearScreen()
            if (self.life_stage == "baby"):
                print(baby_pet[4])
            elif (self.life_stage == "child"):
                print(child_pet[4])
            elif (self.life_stage == "teen"):
                print(teen_pet[4])
            else:
                print(adult_pet[4])
            idle_sleep()
            print() 
            
            print(self.name,"is sleeping...")
            time.sleep(2)
            
            clearScreen()
            if (self.life_stage == "baby"):
                print(baby_pet[4])
            elif (self.life_stage == "child"):
                print(child_pet[4])
            elif (self.life_stage == "teen"):
                print(teen_pet[4])
            else:
                print(adult_pet[4])
            print("Your pet is named",'\033[1m'+self.name+'\033[0m',"and its age is",'\033[1m'+str(self.age)+'\033[0m'+".")
            print("Your pet's life stage is:",'\033[1m'+self.life_stage+'\033[0m')
            self.birthday()
            print()
            self.print_stats()
            
            print()
            print(self.name,"is still sleeping...")
            time.sleep(2)
            self.sleep_need = 100
            dead = self.health_life_check()
            
            if (dead == False):
                clearScreen()
                if (self.life_stage == "baby"):
                    print(baby_pet[5])
                elif (self.life_stage == "child"):
                    print(child_pet[5])
                elif (self.life_stage == "teen"):
                    print(teen_pet[5])
                else:
                    print(adult_pet[5])
                print("Your pet is named",'\033[1m'+self.name+'\033[0m',"and its age is",'\033[1m'+str(self.age)+'\033[0m'+".")
                print("Your pet's life stage is:",'\033[1m'+self.life_stage+'\033[0m')
                self.birthday()
                print()
                self.print_stats()
                
                print()
                print(self.name,"is awake!")
                slept_recently = True
                time.sleep(2)
                print()
            
            else:
                pass

    #This lets you give your pet medicine if it's sick and retsores its health need
    def medicine(self):
        print()
        if (self.health_need >= 75):
            print(self.name,"isn't sick!")
            time.sleep(2)
            print()
        else:
            clearScreen()
            if (self.life_stage == "baby"):
                print(baby_pet[8])
            elif (self.life_stage == "child"):
                print(child_pet[9])
            elif (self.life_stage == "teen"):
                print(teen_pet[9])
            else:
                print(adult_pet[9])
            print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
            print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
            pet.birthday()
            print()
            pet.print_stats()
            print()

            self.health_need += 50
            print("Giving",self.name,"medicine...")
            time.sleep(2)
            print()

    def health_life_check(self):
        if (self.age >= 55 and self.hunger_need > 0 and self.health_need > 0): #This allows your pet to die of old age
            death_chance = random.random()
            if (death_chance > 0.97):
                elder_death = True
                return True
            else:
                return False
        elif(self.hunger_need <= 0 or self.health_need <= 0): #This allows you pet to run away/die if neglected
            return True
        else:
            return False

    def assign_personality(self): #assigns your pet a personality upon aging up to child based on its stats
        if (self.fun_need <= 45):
            self.personality = 'restless' #restless pets get bored faster

        elif(self.clean_need <= 45):
            self.personality = 'messy' #messy pets get dirty faster

        elif (self.hunger_need <= 45):
            self.personality = 'greedy' #greedy pets get hungry faster

        elif (self.health_need <= 65):
            self.personality = 'sickly' #sickly pets lose health more easily

        elif (self.fun_need >= 75):
            self.personality = 'carefree' #cheerful pets get bored slower

        elif (self.clean_need >= 75):
            self.personality = 'neat' #neat pets stay clean longer

        elif (self.hunger_need >= 70 and self.fun_need >= 70 and self.health_need >= 75 and self.clean_need >= 70):
            self.personality = 'balanced' #balanced pets have slower need drain across the board
        
        else:
            self.personality = 'normal' #no affect on stats

    def birthday(self): #This checks for your pet's age to print birthdays and age them up
        if (self.age < 51):
            if (self.age == 5 or self.age == 15 or self.age == 25 or self.age == 50):
                self.assign_personality()
                print('\033[1m'+self.name+'\033[0m',"is aging up today!")
                if (self.age == 5):
                    self.life_stage = "child"
                    self.d = 15
                elif (self.age == 15):
                    self.life_stage = "teen"
                    self.d = 25
                elif (self.age == 25):
                    self.life_stage = "adult"
                    self.d = 50
                elif (self.age == 50):
                    self.life_stage = "elder"
            elif (self.age == 6 or self.age == 16 or self.age == 26):
                print('\033[1m'+self.name+'\033[0m',"will age up in",'\033[1m'+str(self.d-self.age)+'\033[0m',"day(s)! Its personality is now:", '\033[1m'+self.personality+'\033[0m')
            else:
                print('\033[1m'+self.name+'\033[0m',"will age up in",'\033[1m'+str(self.d-self.age)+'\033[0m',"day(s)!")
        else:
            print('\033[1m'+self.name+'\033[0m',"isn't aging up anymore.")
    
    def life_stage_check(self): #checks for pet's age and returns it as a number used in the idle_action function
        
        if (self.life_stage == "baby"):
            return 1
        elif (self.life_stage == "child" or self.life_stage == "teen"):
            return 2
        elif (self.life_stage == "adult"):
            return 3
        elif (self.life_stage == "elder"):
            return 4

def print_instructions(): #prints the game instructions
    clearScreen()
    print("PyPet is a simple virtual pet simulator designed in the style of Tamagotchi.")
    print("Taking good care of your pet involves managing its 5 needs: Hunger, Fun, Hygiene, Sleep, and Health.")
    print(baby_pet[0])    
    print("Your pet is named",'\033[1mExample\033[0m',"and its age is",'\033[1m0\033[0m'+".")
    print("Your pet's life stage is:",'\033[1m baby \033[0m')
    print('\033[1mExample\033[0m',"will age up in",'\033[1m5\033[0m',"day(s)!")
    print()
    print("Hunger:   100")
    print("Fun:      100")
    print("Hygiene:  100")
    print("Sleep:    100")
    print("Health:   100")
    print()
    print("Hint: Pay attention to the pet potrait! If one or more of your pet's needs is low, it will look unhappy!")
    print()
    print("There are seven options you can use every time the game asks what you would like to do:")
    print()
    print("Type 'f' or 'feed' to feed your pet. This restores hunger.")
    print("Type 'p' or 'play' to play with your pet. This restores fun.")
    print("Type 'c' or 'clean' to give your pet a bath. This restores hygiene.")
    print("Type 's' or sleep to send your pet to bed. This restores sleep.")
    print("Type 'h' or 'heal' to give your pet medicine. This restores health.")
    print("Type 'n' or 'none' to leave your pet to its own devices. It may do something that negatively or positively affects its needs.")
    print("Type 'help' to see this list of commands again.")
    print()
    print("Your pet's needs will be affected every time you take (or don't take!) action.")
    print("Your pet's health need is only adversely affected if it's hunger and/or hygiene is low, or from its own actions.")
    print("Your pet will age by one day every time it sleeps, whether you send it to bed or it passes out from lack of sleep.")
    print("Be especially mindful of your pet's stats near its birthday -- how you take care of it can determine its personality!")
    print("Take good care of your pet, and it will live a long and happy life! But if you neglect it...well...")
    print()

def print_commands(): #prints all the commands you can use
    print()
    print("Type 'f' or 'feed' to feed your pet.")
    print("Type 'p' or 'play' to play with your pet.")
    print("Type 'c' or 'clean' to give your pet a bath.")
    print("Type 's' or sleep to send your pet to bed.")
    print("Type 'h' or 'heal' to give your pet medicine.")
    print("Type 'n' or 'none' to leave your pet to its own devices.")
    print("Type 'help' to see this list of commands again.")
    print()
    input("Press Enter to continue...")

def pass_out(): # Your pet will pass out if it gets too tired
        print(pet.name,"passed out from exhaustion!")
        pet.sleep_need = 50
        pet.fun_need -= 50
        pet.age += 1
        time.sleep(2)
        print()
        print(pet.name,"woke up! But passing out is no fun :(")
        time.sleep(2)

def idle(): #This prints your pet's stats, checks to make sure they aren't going to die, and performs stat decay
    print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
    print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
    pet.birthday()
    print()
    pet.print_stats()
    pet.need_decay()
        
def idle_sleep(): #This does the same thing but only when your pet is asleep
    print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
    print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
    pet.birthday()
    print()
    pet.print_stats()
    
    pet.need_decay_sleep()

def idle_action(): #This decides what your pet will do if you don't give a command. This is based on its needs and age

    age_set = pet.life_stage_check()

    if (age_set == 1):
        if (pet.sleep_need < 60): #if your pet is sleepy, it may nap
            idle_action = random.randint(1,5)
        else:
            idle_action = random.randint(2,5)
    else:
        if (pet.sleep_need < 60): #if your pet is sleepy, it may nap
            idle_action = random.randint(1,7)
        elif (pet.hunger_need < 40): #if your pet is hungry or greedy, it may try to find food
            idle_action = random.randint(2,6)
        elif (pet.hunger_need < 80 and pet.personality == "greedy"):
            idle_action = random.randint(2,6)
        elif (pet.sleep_need < 60 and pet.hunger_need < 40): #if it's both, it might try either
            idle_action = random.randint(1,7)
        else: 
            idle_action = random.randint(2,6)

    if (idle_action == 1):
        print(pet.name,"took a nap.")
        pet.sleep_need += 20
        time.sleep(2)

    elif (idle_action == 2):       
        print(pet.name,"lazes around for a while.")
        pet.sleep_need += 5
        time.sleep(2)

    elif (idle_action == 3):
        print(pet.name,"ran around in circles for a bit.")
        pet.fun_need += 25
        time.sleep(2)

    elif (idle_action == 4):
        print(pet.name,"stares at the wall for a while. It's very boring.")
        pet.fun_need -= 15
        time.sleep(2)

    elif (idle_action == 5):
        print(pet.name,"entertains itself for a bit.")
        if (pet.personality == "carefree" or pet.personality == "balanced"):
            pet.fun_need += random.randint(5,15)
        else:
            pet.fun_need += random.randint(2,10)
        time.sleep(2)
    
    elif (idle_action == 6):
        outside = random.randint(1,3)
        if (outside == 1):
            print(pet.name,"decided to wander around, and they had a good time!")
            pet.fun_need += 30
            time.sleep(2)
        elif (outside == 2):
            print(pet.name,"decided to wander around, but they didn't find anything cool.")
            pet.fun_need -= 10
            time.sleep(2)
        elif (outside == 3 and pet.health_need >= 70):
            print(pet.name,"decided to wander around, but they got hurt!")
            pet.fun_need -= 15
            if (pet.personality == "sickly"):
                pet.health_need -= random.randint (10,20)
            else:
                pet.health_need -= random.randint(5,15)
            time.sleep(2)
        else: 
            print(pet.name,"decided to wander around, but they didn't find anything cool.")
            pet.fun_need -= 10
            time.sleep(2)
    
    elif (idle_action == 7):
        if (pet.personality == "balanced"):
            food = random.randint(1,2)
        else:
            food = random.randint(1,3)
        if (food == 1):
            print(pet.name,"searched around your kitchen and found some food.")
            pet.hunger_need += random.randint(5,20)
            time.sleep(2)
        elif (food == 2):
            print(pet.name,"searched around your house to find some food, but they didn't find anything.")
            pet.fun_need -= random.randint(1,5)
            time.sleep(2)
        elif (food == 3 and pet.health_need >= 70):
            print(pet.name,"searched around your house and ate something that wasn't actually food!")
            if (pet.personality == "sickly"):
                pet.health_need -= random.randint (10,20)
            else:
                pet.health_need -= random.randint(5,15)
                time.sleep(2)

def number_game(): #A simple number guessing game you can play with your pet to fill the fun need

    won = False
    guesses = 0

    print(pet.name,"is thinking of a number between 0 and 100...")
    num = random.randint(0,100)
    print()
    print("Now it's up to you to guess what it is!")
    print()

    while (won == False):
        try:
            num_guess = int(input("What number do you think it is?"))
            guesses += 1
        except:
            print()
            print("That's not a number! Try again!")
            print()
            continue

        if (num_guess > 100 or num_guess < 0):
            print("That's not a number between 1 and 0!")
            print()
            continue

        elif (num_guess != num):
            if (num_guess > num):
                if (abs(num - num_guess)  <= 10):
                    print("Nope, your guess is a little too high, but you're very close. Try again!")
                    print()
                
                elif (abs(num - num_guess)  <= 25):
                    print("Nope, that's a little too high! Try again!")
                    print() 

                elif (abs(num - num_guess)  <= 50):
                    print("Nope, that's too high! Try again!")
                    print()

                elif (abs(num - num_guess) <= 100):
                    print("Nope, that's way too high! Try again!")
                    print()
                
                continue
        
            elif (num_guess < num):
                if (abs(num - num_guess)  <= 10):
                    print("Nope, your guess is a little too low, but you're very close. Try again!")
                    print()
                
                elif (abs(num - num_guess)  <= 25):
                    print("Nope, that's a little too low! Try again!")
                    print() 

                elif (abs(num - num_guess)  <= 50):
                    print("Nope, that's too low! Try again!")
                    print()

                elif (abs(num - num_guess) <= 100):
                    print("Nope, that's way too low! Try again!")
                    print() 
                
                continue

        elif(num_guess == num):
            print()
            won = True
            print("That's correct! It took you",guesses,"tries to figure it out!")
            break

while (playing == True): #This loop contains the actual gameplay

    clearScreen()
    print(other_pet[0])
    print("Welcome to PyPet!")
    game_start = True

    while (game_start == True):
        start = str(input("Would you like to read the instructions? y/n"))

        if (start == 'y'):
            instructions = True
            break

        elif (start == 'n'):
            instructions = False
            break

        else:
            print("Sorry, I didn't get that.")
            continue

    if (instructions == True):
        print_instructions()
        input("Press Enter to start the game...")

        clearScreen()
        print(other_pet[0])
        print("Welcome to PyPet!")
        pass

    elif (instructions == False):
        pass

    name_loop = True #This asks you to name your pet and asks if you're sure
    while (name_loop == True):

        temp = str(input("Please name your PyPet!"))
        temp = temp.capitalize()
        name_confirm = str(input("Your pet will be named "+temp+". Is that correct? y/n"))

        if (name_confirm == 'y'):
            pet = pypet(temp)
            print()
            if (pet.name == 'Debug_pet'): #naming the pet 'Debug_pet' enables cheats that make testing the game easier
                debug = True
                print("Enabling debug cheats...")
            else:
                debug = False  
                print("That's a wonderful name!")
            time.sleep(1)
            print()
            print(pet.name,"is hatching!")
            time.sleep(2)
            break

        elif (name_confirm == 'n'):
            print("Okay, you can enter the name again.")
            print()
            continue
        
        else:
            print("Sorry, I didn't get that.")
            continue

    clearScreen()

    print(baby_pet[0])    
    print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
    print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
    pet.birthday()
    print()
    pet.need_decay()
    pet.age = 0
    pet.print_stats()

    while (dead == False):
        
        dead = pet.health_life_check() #checks to make sure that your pet hasn't died

        if (dead == True):
            playing = False
            break
        else:
            clearScreen()
            
            if (pet.life_stage == "baby"):
                if (pet.clean_need < 35):
                    print(baby_pet[6])
                elif (pet.fun_need < 20 or pet.hunger_need < 40 or pet.sleep_need < 40 or pet.health_need < 60):
                    print(baby_pet[7])
                else:
                    print(baby_pet[0])
            elif (pet.life_stage == "child"):
                if (pet.clean_need < 35):
                    print(child_pet[6])
                elif (pet.fun_need < 20 or pet.hunger_need < 40 or pet.sleep_need < 40 or pet.health_need < 60):
                    print(child_pet[7])
                else:
                    print(child_pet[0])

            elif (pet.life_stage == "teen"):
                if (pet.clean_need < 35):
                    print(teen_pet[6])
                elif (pet.fun_need < 20 or pet.hunger_need < 40 or pet.sleep_need < 40 or pet.health_need < 60):
                    print(teen_pet[7])
                else:
                    print(teen_pet[0])

            else:
                if (pet.clean_need < 35):
                    print(adult_pet[6])
                elif (pet.fun_need < 20 or pet.hunger_need < 40 or pet.sleep_need < 40 or pet.health_need < 60):
                    print(adult_pet[7])
                else:
                    print(adult_pet[0])

            idle()
            print() 

            if(pet.sleep_need < 10):
                print()
                pass_out()
                continue

            elif (pet.sleep_need >= 10):
                while True:
                    action = input("What would you like to do? (Type 'help' for a list of commands.)")
                    
                    if (debug == True):
                        if (action == 'f' or action == 'feed'):
                            pet.feed()
                            break
                        elif (action == 's' or action == 'sleep'):
                            pet.sleep()
                            break
                        elif (action == 'c' or action == 'clean'):
                            pet.clean()
                            break
                        elif (action == 'p' or action == 'play'):
                            pet.play()
                            break
                        elif (action == 'h' or action == 'heal'):
                            pet.medicine()
                            break
                        elif (action == 'n' or action == 'none'):
                            print()
                            idle_action()
                            break 
                        elif (action == 'help'):
                            print_commands()
                            continue

                        elif (action == "set_age"): #cheat code for testing
                            print()
                            pet.age = int(input("How many days old do want Debug_pet to be?"))
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            break

                        elif (action == "age_baby"): #cheat code for testing
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.age = 0
                            pet.life_stage = "baby"
                            break
                        
                        elif (action == "age_child"): #cheat code for testing
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.age = 6
                            pet.life_stage = "child"
                            break
                        
                        elif (action == "age_teen"): #cheat code for testing
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.age = 16
                            pet.life_stage = "teen"
                            break
                    
                        elif (action == "age_adult"): #cheat code for testing
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.age = 26
                            pet.life_stage = "adult"
                            break

                        elif (action == "age_elder"): #cheat code for testing
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.age = 51
                            pet.life_stage = "elder"
                            break

                        elif (action == "stat_drain_hunger"): #cheat code for testing (good for testing the low-need potraits and death system)
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.hunger_need = 10
                            break

                        elif (action == "stat_drain_health"): #cheat code for testing (good for testing the low-need potraits and death system)
                            print()
                            print("Applying cheat code...")
                            time.sleep(1.5)
                            pet.health_need = 10
                            break
                        else:
                            print()
                            print("Sorry, I don't understand.")
                            print()
                            continue

                    else:
                        if (action == 'f' or action == 'feed'):
                            pet.feed()
                            break
                        elif (action == 's' or action == 'sleep'):
                            pet.sleep()
                            break
                        elif (action == 'c' or action == 'clean'):
                            pet.clean()
                            break
                        elif (action == 'p' or action == 'play'):
                            pet.play()
                            break
                        elif (action == 'h' or action == 'heal'):
                            pet.medicine()
                            break
                        elif (action == 'n' or action == 'none'):
                            print()
                            idle_action()
                            break 
                        elif (action == 'help'):
                            print_commands()
                            continue

                        else:
                            print()
                            print("Sorry, I don't understand.")
                            print()
                            continue

    #All the stuff down here is what displays if your pets runs away (baby) or dies (child or older), effectively ending the game unless you start over

    clearScreen()

    if (pet.life_stage == "baby"):
        print(other_pet[1])
    elif (pet.life_stage == "child"):
        print(child_pet[8])    
    elif (pet.life_stage == "teen"):
        print(teen_pet[8])
    else:
        print(adult_pet[8])

    print("Your pet is named",'\033[1m'+pet.name+'\033[0m',"and its age is",'\033[1m'+str(pet.age)+'\033[0m'+".")
    print("Your pet's life stage is:",'\033[1m'+pet.life_stage+'\033[0m')
    pet.birthday()
    print()
    pet.print_stats()
    print()
    time.sleep(1)
    if (pet.life_stage == "baby"):
        print(pet.name,"ran away...were you keeping it healthy and well-fed?")
        print()
        time.sleep(2)
        print("It is a sad day indeed...")
    elif (elder_death == True):
        print(pet.name,"has passed away...it lived a long life under your care.")
        print()
        time.sleep(2)
        print("It is a sad day, but you gave it a good life.")
    else:
        print(pet.name,"has passed away...were you keeping it healthy and well-fed?")
        print()
        time.sleep(2)
        print("It is a sad day indeed...")

    while (dead == True):

        time.sleep(2)
        print()
        play_again = str(input("Would you like to start over with a new pet? y/n"))

        if (play_again == 'y'):
            print("Okay, let's start over.")
            dead = False
            playing = True
            break

        elif (play_again == 'n'):
            print("Quitting PyPet...")
            time.sleep(1)
            quit()
        
        else:
            print("Sorry, I didn't get that.")
            continue