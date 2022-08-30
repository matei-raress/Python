from concurrent.futures import ProcessPoolExecutor

# un thread pool care sa fie: auto-closeable, sa implementeze functia map care sa distribuie automat volumul de  lucru, sa implementeze functiile de join si terminate
def counter(list_of_integers):

    for i in range(0, list_of_integers):
        print(i)
    return 0


def test_process_pool_executor(function, list_of_integers):
    with ProcessPoolExecutor(4) as pool:
       return  pool.map(function, list_of_integers)



if __name__ == '__main__':
    list_of_integers = [10, 11, 12, 13, 14, 15, 16, 17, 18]
    test_process_pool_executor(counter, list_of_integers)
    print()
