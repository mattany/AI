import sys


def write_propositions(domain_file, disks, pegs):
    domain_file.write("Propositions:\n")
    for i in disks:
        domain_file.write("%s " % i)
        for j in pegs:
            domain_file.write("%s%s " % (i, j))
    for i, disk1 in enumerate(disks):
        for j in range(i + 1, len(disks)):
            domain_file.write("%s%s " % (disk1, disks[j]))
    for i in pegs:
        domain_file.write("%s " % i)
    domain_file.write("\n")


def write_actions(domain_file, disks, pegs):
    domain_file.write("Actions:\n")
    for i, disk in enumerate(disks):
        for j in range(i + 1, len(disks)):
            for k in range(j + 1, len(disks)):
                add_action(domain_file, disk, disks[j], disks[k])
                add_action(domain_file, disk, disks[k], disks[j])
        for j, peg1 in enumerate(pegs):
            for k, peg2 in enumerate(pegs):
                if j != k:
                    add_action(domain_file, disk, peg1, peg2)
        for j, peg in enumerate(pegs):
            for k in range(i + 1, len(disks)):
                add_action(domain_file, disk, peg, disks[k])
                add_action(domain_file, disk, disks[k], peg)


def add_action(domain_file, disk, src, dest):
    domain_file.write("Name: %s%s%s\n" % (disk, src, dest))
    domain_file.write("pre: %s %s %s%s  \n" % (disk, dest, disk, src))
    domain_file.write("add: %s %s%s\n" % (src, disk, dest))
    domain_file.write("delete: %s %s%s\n" % (dest, disk, src))


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    write_propositions(domain_file, disks, pegs)
    write_actions(domain_file, disks, pegs)
    domain_file.close()


def write_initial_state(problem_file, disks, pegs):
    problem_file.write("Initial State: ")
    problem_file.write("%s " % disks[0])
    for i in range(len(disks) - 1):
        problem_file.write("%s%s " % (disks[i], disks[i+1]))
    problem_file.write("%s%s " % (disks[-1], pegs[0]))
    for i in range(1, len(pegs), 1):
        problem_file.write("%s " % pegs[i])
    problem_file.write("\n")


def write_goal_state(problem_file, disks, pegs):
    problem_file.write("Goal State: ")
    problem_file.write("%s " % disks[0])
    for i in range(len(disks) - 1):
        problem_file.write("%s%s " % (disks[i], disks[i + 1]))
    problem_file.write("%s%s " % (disks[-1], pegs[-1]))
    for i in range(0, len(pegs) - 1, 1):
        problem_file.write("%s " % pegs[i])


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    write_initial_state(problem_file, disks, pegs)
    write_goal_state(problem_file, disks, pegs)
    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
