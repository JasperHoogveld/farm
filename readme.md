For my pipeline I have first cloned the github repository to both my local pc and the server in /home/git/farm/

I have created a workflow as below that starts on 'push' and first runs a test to see if the application gives the output as expected.
The workflow first does a 'checkout' of the repository, sets up python and runs the pytest with the requirements in requirements.txt
When that test is completed it continues in that same yaml file with the SSH connection to the server using a keypair that's on the server and starts a deployment script.
The public key is used as deploy key for the bash script.

```
name: Run Tests

on: push
jobs:
  run-tests:
    runs-on: ubuntu-20.04
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Setup Python 3.11
        uses: actions/setup-python@v3
        with:
          python-version: '3.11.0'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
      - name: executing remote ssh commands using password
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |  
                sudo bash /home/deploy.rc 
```

The bash script is simply as below. It changes to the folder where the git repository is, does a pull and copies the python file to the folder that is used by gunicorn. I then restarts the gunicorn service and logs out.

```
#!/bin/bash
cd /home/git/farm/
git pull
cp main.py /home/farm/
systemctl restart farm
exit
```

Three issues solved:
- I wanted to have the SSH connection and deployment in a separate action, but the action would not start with what I have tried (which was a 'check-run'). It still works the same now because the action just stops if the test fails.
- The bash script is ran by the root user which was not my first intention, but trying it with another user gave issues with sudo actions which take a password locally on the server. That probably needs a change to the "/etc/sudoers file", but I could not get that to work in the timeframe I have.
- The SSH connection didn't work until I found the "appleboy/ssh-action@master" action and used it with the secrets.