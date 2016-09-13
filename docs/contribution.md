# Contribution
Any kind of contribution is encouraged, e.g., bug report, question answer, and submit pull-request.

Before taking actions, we highly recommend reading the [doc](docs).


## Bug and Questions

We now have two channels for bug and questions:

* [Jira](https://jira.hyperledger.org): report bug issues.
* [Slack](https://hyperledgerproject.slack.com/archives/fabric-sdk-py): technical discussions.


## Code Commit

The project employs [Gerrit](https://gerrit.hyperledger.org) as the code commit/review system. More details about Gerrit can be learned from the [Hyperledger Fabric Gerrit Doc](https://github.com/hyperledger/fabric/blob/master/docs/Gerrit/).

* Clone the project with your Linux Foundation ID (`LFID`), we suggest clone it into the `$GOPATH/src/github.com/hyperledger` directory so that it will build.

```sh
$ git clone ssh://LFID@gerrit.hyperledger.org:29418/fabric-sdk-py && scp -p -P 29418 LFID@gerrit.hyperledger.org:hooks/commit-msg fabric-sdk-py/.git/hooks/
```

(Optionally) Config your git name and email if not setup previously.

```sh
$ git config user.name "your name"
$ git config user.email "your email"
```

(Optionally) Setup git-review by inputting your LFID. Notice this is only necessary once.
```sh
$ git review -s
```

* Create a descriptively-named branch off of your cloned repository

```sh
$ cd fabric-sdk-py
$ git checkout -b issue-NNNN
```

* Commit your code with `-s` to sign-off, and `-a` to automatically add changes.

```sh
$ git commit -s -a
```

Example commit msg may look like:

```sh
A short description of your change with no period at the end

You can add more details here in several paragraphs, but please keep each line
width less than 80 characters. A bug fix should include the issue number.

Fix Issue #7050.

Change-Id: IF7b6ac513b2eca5f2bab9728ebd8b7e504d3cebe1
Signed-off-by: Your Name <committer@email.address>
```

* Submit your commit using `git review`.

```sh
$ git review
```

After the review is uploaded successfully, you can open [Gerrit Dashboard](https://gerrit.hyperledger.org/r/#/dashboard/self) to invite reviewers for checking. The patch will be merged into the `master` branch if passing the reviewer checking.

* If you need to refine the patch further, you can commit the new code with `git commit -a --amend`, and then repeat the `git review` command.
