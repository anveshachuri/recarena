# Contributing to recarena

Thanks for helping. The best contributions make it easier to answer one question: **can this estimator be trusted on this kind of problem?**

## Good places to start

- Issues labeled [`good first issue`](https://github.com/anveshachuri/recarena/labels/good%20first%20issue) are small, with a clear way to check the result.
- Issues labeled [`research`](https://github.com/anveshachuri/recarena/labels/research) are open questions. Comment with your plan before building one.
- Comment on an issue before you start, so two people don't do the same work.

## Set up

```bash
git clone https://github.com/anveshachuri/recarena.git
cd recarena
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"   # On Linux or macOS: .venv/bin/python
.venv/Scripts/python -m pytest
```

## What a good pull request has

- **One change.** Separate unrelated fixes into separate PRs.
- **A test that fails without your change.** Run it against the old code to be sure.
- **Checks against known answers where possible.** An estimator should have a hand-calculated test, and an unbiased one should also recover the simulator's true value.
- **Honest results.** If you report benchmark numbers, include the exact command and seed, and say what you did not test.
- **No unrelated formatting changes.**

Changing simulator behavior changes every published result. Please keep new behavior off by default, and test that existing settings still produce the same results.

## Adding a new estimator or user model

Open an issue first with a link to the paper or a short description of the method. A new estimator needs:

1. A hand-calculated test on a tiny handmade dataset.
2. A statistical test against `true_value`, if the method claims to be unbiased.
3. A row in the benchmark, with the command you used.

## Using AI tools

AI-assisted contributions are welcome, under the same standards as any other:

- Say in the PR that you used AI and which tool, in one line.
- Run the tests yourself, and only claim what you actually ran.
- Read the whole change, and be ready to explain and revise it.
- Don't open issues or PRs in bulk. Only report problems you have reproduced.

PRs that don't meet these standards may be closed without detailed review.

## License

By contributing, you agree that your work is licensed under the [Apache-2.0 License](LICENSE).
