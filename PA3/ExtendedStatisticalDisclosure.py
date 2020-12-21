# Import round data and setup
import re
from string import ascii_lowercase

# Change this to the round data file
data_set = "target-rounds"

users = []
for letter in tuple(ascii_lowercase):
    for i in range(0,10):
        users.append(letter + str(i))

targets = tuple(filter(lambda x: x[1] == str(0), users))

senders = []
receivers = []
with open(data_set, "r") as infile:
    for line in infile:
        senders.append(re.findall("\'(.*?)\'", line))
        receivers.append(re.findall("\'(.*?)\'", infile.readline()))

# %% [markdown]
# # Extended Statistical Disclosure Attack
#  - Given a set of targets, for each target observe $t'$ batches where target did not send
#  - For each batch $i$, make the vector $\overline{u_{i}}$ where:
#     - Each element corresponds to a mix user (260 elements in this case)
#     - Elements are $1/b$ if the user received a message this round, where $b$ is batch size
#     - Elements are 0 if the user did not
#  - Background distribution $\overline{U}$ can then be estimated as: $$\overline{U} = \frac{1}{t'} \sum_{i=1}^{t'} \overline{u_{i}}$$
#  
# %% [markdown]
# Next, for each target observe $t$ batches where the target sends $m_{i}$ messages
#  - For each batch $i$, make the vector $\overline{o_{i}}$ where:
#     - Each element corresponds to a mix user (260 elements)
#     - Elements are $1/b$ if the user received a message this round, where $b$ is batch size
#     - Elements are 0 if the user did not
#  - Compute observation $\overline{O}$ as: $$\overline{O} = \frac{1}{t} \sum_{i=1}^{t}\overline{o_{i}}$$
#  - Compute $\overline{m}$ as: $$\overline{m} = \frac{1}{t} \sum{m_{i}}$$
# 

# %%
U_per_target = []
O_per_target = []
m_per_target = []
for target in targets:
    u_i_set = []
    o_i_set = []
    m_i_set = []
    for i_send, i_receive in zip(senders, receivers):
        if target in i_send:
            o_i = []
            for user in users:
                if user in i_receive:
                    o_i.append(1/32)
                else:
                    o_i.append(0)
            m_i_set.append(i_send.count(target))
            o_i_set.append(o_i)
        else:
            u_i = []
            for user in users:
                if user in i_receive:
                    u_i.append(1/32)
                else:
                    u_i.append(0)
            u_i_set.append(u_i)
    
    t_prime = len(u_i_set)
    U = [sum(i) for i in zip(*u_i_set)]
    U = list(map(lambda x: (1/t_prime)*x, U))
    U_per_target.append(U)

    t = len(o_i_set)
    m = sum(m_i_set) * (1/t)
    m_per_target.append(m)
    O = [sum(i) for i in zip(*o_i_set)]
    O = list(map(lambda x: (1/t)*x, O))
    O_per_target.append(O)
        

# %% [markdown]
# Now that all observations are completed, the behavior vector $\overline{v}$ of the target can be estimated as: $$\overline{v} = \frac{1}{\overline{m}} [b * \overline{O} - (b - \overline{m})\overline{U}]$$

# %%
v_per_target = []
# m is scalar, U and O are 1d 260 mag vectors, v will be 1d 260 mag vector
for target, U, O, m in zip(targets, U_per_target, O_per_target, m_per_target):
    b_O = list(map(lambda x: x*32, O))
    b_m_U = list(map(lambda x: x*(32-m), U))
    square_brackets = []
    for i, j in zip(b_O, b_m_U):
        square_brackets.append(i - j)
    v = list(map(lambda x: (1/m) * x, square_brackets))
    v_per_target.append(v)

# %% [markdown]
# Finally, the top two probabilities from each v are picked out, and the corresponding users are predicted to be the friends of the target in $v$. Results are stored in an array for each target.

# %%
friends = []
for target, v in zip(targets, v_per_target):
    # We'll say the likey friends are the top two probablities
    zipped = zip(users, v)
    friendranks = sorted(zipped, key=lambda x: x[1])
    friends.append([ friendranks[-1][0], friendranks[-2][0] ])


# %%
if data_set == "example-rounds":
    # Check the results against the key
    friends_key = []
    with open("example-truth", "r") as infile:
        vals = re.findall("\'(.*?)\'", infile.read())
        for idx, val in enumerate(vals):
            if idx % 3 == 0 or idx % 3 == 1:
                continue
            friends_key.append([vals[idx-1], val])
    # scoring
    points = 0
    for user, key, guess in zip(targets, friends_key, friends):
        u_points = 0
        if key[0] in guess:
            u_points += 1
        if key[1] in guess:
            u_points += 1
        points += u_points
        print(user + ": " + str(u_points) + "/2 correct")
        print("     Guess: " + guess[0] + ", " + guess[1])
        print("     Actual: " + key[0] + ", " + key[1])
    print("Total score: " + str(points) + "/52")
else:
    # Export to CSV, format is target,f1,f2
    with open("results.csv", "w") as outfile:
        lines = []
        for target, guess in zip(targets, friends):
            lines.append(target + "," + guess[0] + "," + guess[1] + "\n")
        outfile.writelines(lines)


