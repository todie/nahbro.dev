# nahbro.dev

nah bro as a service.

there are a lot of robots. they want your content.
nahbro.dev generates the files that ask them to leave.

## use it

```sh
curl -s https://nahbro.dev/robots.txt > public/robots.txt
curl -s https://nahbro.dev/llms.txt   > public/llms.txt
```

or get everything at once:

```sh
curl -s https://nahbro.dev/generate
```

## what's in it

every named AI crawler — GPTBot, ClaudeBot, Bytespider, CCBot, and the rest.
full list in [src/generators/robots.ts](src/generators/robots.ts).
when a new one shows up, send a PR.

## does it work

some of them will listen. the rest will not.
the files are here either way.

## run it

```sh
git clone https://github.com/todie/nahbro.dev
cd nahbro.dev
npm install
npm run dev
```

## license

MIT
