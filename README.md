# portfolio_yassine

**Yassine | Application Security Research & Systems Programming**

A no-build technical portfolio collecting independent application-security investigations, reproducible labs, and C projects.

**Website:** https://bossyassine78-ship-it.github.io/portfolio_yassine/

## Research

Eight original investigations, presented as anonymized case studies under [Investigations](research/index.html):

- Identity lifecycle / email change
- Identity provider routing / OIDC
- GraphQL aliases and rate-limiting hypotheses
- OAuth redirect chaining
- Checkout price integrity
- HTML injection in registration flows
- Clickjacking / UI redressing
- Authentication callback open redirect (independently reproduced; resolved)

Each case documents the hypothesis, trust boundary, technical request or flow, available evidence, reviewer outcome, and limits. **Examples are clearly marked synthetic reconstructions**, not verbatim captures of real applications. Not every hypothesis was accepted or demonstrated exploitable impact.

## Engineering projects

- **Authorization Boundary Lab:** a localhost-only Python HTTP API with deliberately vulnerable and fixed modes. Explores BOLA, broken function-level authorization, and account deletion state. Source and automated tests under [`labs/authz-lab`](labs/authz-lab/).
- **Session Lifecycle Demo:** interactive client-side state-machine exercise.
- **[libft](https://github.com/bossyassine78-ship-it/libft):** C memory/string/list implementation.
- **[printf_checker](https://github.com/bossyassine78-ship-it/printf_checker):** test utility for C `printf` implementations.
- **ft_printf:** C variadic formatting implementation (work in progress, private source).

## Run locally

From the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Visit http://127.0.0.1:8000. To run the test suite:

```bash
cd labs/authz-lab
python3 -m unittest -v test_lab.py
```

## Responsible disclosure

Production targets, report IDs, private cookies or credentials, and raw traffic from confidential submissions are not included. Anonymization reduces identifying details but does not guarantee that a distinctive case cannot be recognized. Publication should respect the applicable programs' disclosure rules.

## Source layout

`index.html` homepage · `research/` investigations and technical reports · `labs/` runnable exercises · `assets/` visual style and JavaScript.


## Contact & services

The public site includes `notes.html`, `services.html` and `contact.html` with the editorial design. The contact form is plain HTML, posting to FormSubmit. FormSubmit requires a **one-time destination-email confirmation** after the first submission before email notifications start. The target address is present in the public HTML source. It can later be replaced with FormSubmit's random alias to avoid exposing the email in markup. Keep CAPTCHA on to reduce bot spam.

Do **not** commit private bounty report exports, screenshots, attachments, credentials, session tokens, or original program-specific evidence to this public repository. Deleting files from the branch does not erase old Git history; any past exposure requires a separate history-remediation assessment.
