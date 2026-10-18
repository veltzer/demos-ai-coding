# Intent: a secret cheat code

*From: Product. For: the games team. Change name: `cheat-code`.*

## Why

Tic-tac-toe has been live for a month. People play, but Hard can never be
beaten, and many players quit after two or three draws. Players love
secrets they can share with friends: we want a hidden cheat code that lets
you beat the computer once in a while. Players will pass the code around,
which brings them back to the page and brings their friends.

## What we want

- A secret code typed on the keyboard during a game against the computer
  unlocks a cheat for that game: the player may **steal** one square from
  the computer. The computer's mark on that square becomes the player's
  mark, and that counts as the player's move.
- One steal per game. It is never shown or hinted at on the page until the
  code has been typed. After that, the page makes clear how to use it.
- The code is the classic one: up, up, down, down, left, right, left, right,
  B, A.
- A game won with a steal is announced differently ("You won... with a
  little help"), and it is counted separately in the score. It must not
  count as a normal win.
- The cheat works only against the computer, at both levels, and not when
  two friends play on the same screen.

## What must not change

- Without the code, the game behaves exactly as it does today, and Hard
  still never loses to fair play.
- On the page, nobody can steal without typing the code. Nobody can steal
  twice in a game, even by sending requests to the server by hand.

## How we will know it worked

- It is live in production, the old game unchanged.
- People share the code: we see steals in games we did not set up ourselves.
