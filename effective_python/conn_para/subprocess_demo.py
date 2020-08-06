"""
@author: magician
@file:   subprocess_demo.py
@date:   2020/8/6
"""
import os
import subprocess
import time


def run_sleep(period):
    """
    run_sleep
    @param period:
    @return:
    """
    proc = subprocess.Popen(['sleep', str(period)])
    return proc


def run_openssl(data):
    """
    run_openssl
    @param data:
    @return:
    """
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Q13S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure the child gets input

    return proc


def run_md5(input_stdin):
    """
    run_md5
    @param input_stdin:
    @return:
    """
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE,
    )

    return proc


if __name__ == '__main__':
    proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    print(out.decode('utf-8'))

    proc1 = subprocess.Popen(['sleep', '0.3'])
    while proc.poll() is None:
        print('Working...')
    print('Exit status', proc.poll())

    start = time.time()
    procs = []
    for _ in range(10):
        proc = run_sleep(0.1)
        procs.append(proc)

    for proc in procs:
        proc.communicate()
    end = time.time()
    print('Finished in %.3f seconds' % (end - start))

    procs1 = []
    for _ in range(3):
        data = os.urandom(10)
        proc = run_openssl(data)
        procs1.append(proc)

    for proc in procs1:
        out, err = proc.communicate()
        print(out[-10:])

    input_procs = []
    hash_procs = []
    for _ in range(3):
        data = os.urandom(10)
        proc = run_openssl(data)
        input_procs.append(proc)
        hash_proc = run_md5(proc.stdout)
        hash_procs.append(hash_proc)

    for proc in input_procs:
        out, err = proc.communicate()

    for proc in hash_procs:
        out, err = proc.communicate()
        print(out.strip())

    proc = run_sleep(10)
    try:
        proc.communicate(timeout=0.1)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait()

    print('Exit status', proc.poll())
