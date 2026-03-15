---
sidebar_label: "rfcs PR #188"
sidebar_position: 1
---

# RFC: React Server Components

> **원문 PR**: https://github.com/reactjs/rfcs/pull/188
> **저장소**: reactjs/rfcs | **작성자**: @josephsavona | **상태**: merged
> **생성일**: 2020-12-21 | **머지일**: 2022-10-25
> **변경**: +609 / -0 (1개 파일)
> **라벨**: `CLA Signed`, `react core team`

---

## PR 설명 (원문)

In this RFC, we propose introducing Server Components to React. **We recommend [watching our talk introducing Server Components](https://reactjs.org/server-components) before reading.**

### [View the formatted RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md)

---

## 토론 (199건)

### #1 — @Daniel15 — 2020-12-21 18:41

Will any part of the server-side be tightly coupled to Node.js, or could it run on a different JS runtime (for example, Rhino in Java, embedded V8 like with ClearScript for C#, ChakraCore, etc)?  The only mention of Node in the RFC is around debugging ("you would debug your API in Node") but it's unclear as to whether server-side components would be tightly coupled to Node or not. Perhaps this is intentionally an open question at the moment. One of the major benefits and reasons for popularity of JavaScript is that it runs in lots of places, so it would be unfortunate to couple it to one particular implementation.

It does say this:

> Server Components are designed from the beginning to be used with any meta-framework or into custom application setups

but that's still unclear as to whether "any meta-framework" implicitly means "any Node.js meta-framework"

I see a comparison to the older ASP.NET WebForms technology in the RFC, but it'd be interesting to compare it to ASP.NET Blazor too, which is a newer model where the components can either run server-side or client-side (via compilation to WebAssembly).

---

### #2 — @brandoncroberts — 2020-12-21 19:11

From what I read, meta-frameworks refers to other React Frameworks like Next.js and Gatsby

---

### #3 — @behzad888 — 2020-12-21 19:24

There are some things I really think will help. As I saw, the following questions came up.

## Using SSR
If we use SSR, there will be two scenarios:

 - First, Using SSR and server components at the same time: This absolutely ignores the idea.
 - Second, Using SSR and server components as part of the application: I think this is a challenging idea. Although, this scenario parts our project into two sections, and it's not cheap.
 
 ## Without SSR
We send our texts, images, and many pieces of information using JSON. How should we deal with SEO?

---

### #4 — @josephsavona — 2020-12-21 19:30

NOTE: edited to provide more context

> Will any part of the server-side be tightly coupled to Node.js, or could it run on a different JS runtime

@Daniel15 React Server Components are conceptually decoupled from the JS runtime, but we also need some amount of environment-specific integration. For example, we currently support a Node.js integration for general consumption (used in the demo) and an internal integration for Relay. One of the main aspects of these integrations is handling the interaction between server/client components and packages (more details on that point in the [related RFC](https://github.com/reactjs/rfcs/pull/189)). We can consider adding support for other environments (and are interested in the community's feedback about which we may want to prioritize).

> From what I read, meta-frameworks refers to other React Frameworks like Next.js and Gatsby

@8brandon Yup, we're referring to frameworks such as Next.js and Gatsby. I'll update the text to clarify.

---

### #5 — @markerikson — 2020-12-21 19:34

@josephsavona other half of that question:

how feasible is it for any of this server functionality to work if your backend is _not_ JS-based (ie, Python, Java, Go, etc)?

---

### #6 — @themre — 2020-12-21 19:43

> @josephsavona other half of that question:
> 
> how feasible is it for any of this server functionality to work if your backend is _not_ JS-based (ie, Python, Java, Go, etc)?

Yes, also very interested because this would allow to push for React on many areas where other server tech dominates and cannot be replaced.

---

### #7 — @josephsavona — 2020-12-21 20:18

> how feasible is it for any of this server functionality to work if your backend is not JS-based (ie, Python, Java, Go, etc)?

This an interesting area for potential future exploration. As noted in the RFC, one of the benefits of React Server Components is that they allow developers to use a single language and framework to write an application, and share code across the server and client. We can foresee an ecosystem of packages forming around Server Components (libraries designed to be called from Server Components or Shared Components) which would not be available to developers attempting to use aspects of the Server Components architecture from other languages. Similarly, using a different language for the server would likely prohibit (or at least complicate) code sharing. Further, we expect to continue iterating on the response protocol for Server Components ("streaming JSON with slots") and are not yet ready to standardize it, which would be a prerequisite to making interop libraries for other languages. In summary, this is an interesting idea but it feels a bit premature.

---

### #8 — @aspirisen — 2020-12-21 20:21

Server Components are great idea, it will change the game!
One thing is that it would be pretty good to allow insert Server components into Client components as `memo` component. So every time when the props are changed we request server component to rerender and return the output.

```
import MyServerComponent from "./myServerComponent";

export function ClientComponent() {
  const [id, setId] = React.useState(0);
  return (
    <div>
      <button onClick={() => setId(Math.random())}>Select other id</button>
      <MyServerComponent id={id} />
    </div>
  );
}
```

So there will be pretty seamless integration and it will simple to extract heavy logic to server.

One question is how to `import` server component as you can't literally import this file. 
Maybe something like this 
`const MyServerComponent = React.foreign(() => import('./myServerComponent'));`
So there will be actual HTTP request to server, and server will be able to understand what component it needs and return an export object for react, also this component can be placed on any arbitrary URL. IDE along with TypeScript will understand what component is actually used in `MyServerComponent` variable. In addition you can delegate such kind of code to bundlers or transpilers so they can optimize it if you need, anyway in raw JavaScript that will also work.

---

### #9 — @markerikson — 2020-12-21 20:22

heh, translating:

"It's still experimental, we're still iterating, we're really focused on doing everything in JS for now for simplicity's sake.  We won't rule out it maybe working with other languages, but we're not gonna worry about that for now".

Fair summary?

---

### #10 — @dfabulich — 2020-12-21 20:25

The "why not use async/await" section of the FAQ IMO needs more detail. I think y'all have made the wrong call here.

> **Why don’t use just use async/await?**
> We’d still need a layer on top, for example, to deduplicate fetches between components within a single request. This is why there are wrappers around async APIs. You will be able to write your own. We also want to avoid delays in the case that data is synchronously available -- note that async/await uses Promises and incurs an extra tick in these cases.

A layer to deduplicate fetches sounds great, but that library could use async/await, too.

As it stands, libraries like `react-fs` and `react-fetch` appear to be synchronous, and they *might* be synchronous, depending on the status of the cache, but they might _not_ be synchronous; there's no user-visible way to know. https://github.com/facebook/react/blob/master/packages/react-fs/src/ReactFilesystem.js

(To be clear, right now the code is using a, uh, *very surprising* pattern to make asynchronous code appear synchronous: if the result value is cached, it returns the value synchronously, but if not, the fetcher *throws a Promise*. You know, you'd normally throw exception objects, but JS lets you throw any value, so why not throw a *Promise* amirite?!? When React catches a Promise (a thenable) it awaits the result, caches it and then re-runs the React component; now the component *won't* throw a Promise and will run to completion normally.)

Using async/await will make this code substantially easier to understand, and the cost of a "tick" is trivial (and worth the price, especially in server components).

EDIT: Thinking about this a bit harder, I know the React team has been extremely resistant to async/await in components for years now. Fine. But that needs its own RFC. Some clear written document spelling out in detail why async/await is the wrong approach for React, and not just a comment on this RFC.

I'd like to ask the React team to write that RFC doc because I think it can't be written: you'll find that the argument falls apart when you try to explain it.

---

### #11 — @josephsavona — 2020-12-21 20:27

@markerikson I appreciate that you're trying to get a clear takeaway. However, there are a lot of considerations here and I worry that trying to distill the complex tradeoffs I alluded to into a short summary may not be helpful to folks.

---

### #12 — @ShanonJackson — 2020-12-21 20:45

My initial thoughts after watching the video are this:

All Components in peoples projects can either be thought of as 'Isomorphic' if that codebase is using server-side rendering, OR if that code base is not using serer side rendering then they're all 'client' components. For me personally I feel that introducing an API like this will now cause a abstraction layer where people using server side rendering will now need to think about 3 kinds of components instead of 1 (server/client/isomorphic) and the complexity of thinking about which 'context' you're in because in some contexts you can now only use JSON serializable properties.

For me and our team currently the biggest problem we have is scaling React applications which seems to start getting very hard around the (100+ routes) mark, I feel like this RFC although helps performance it hurts scalability as now we need to consider the implementations and find bugs in 3 types of components instead of 1.

Would be good to hear other peoples thoughts on this.

These are some observations on the API which are purely based on my opinion:

## BundleSize / Server side code.
- Removing a 83KB (20KB gzip) library isn't a big deal, I would say the bigger problem here is that you're using a 83KB library to format dates.
- There's already methods to remove these libraries and allow for sever side code
1: babel-plugin-preval allows you to use server-side code (at build time).
2: NextJS has an implementation for getServerSideProps (server) and getInitialProps (isomorphic) that use the current implementation of React to achieve server side code, and potentially tree shaking in a very simple abstraction.
```ts
// tree shakes out date-fns
ComponentName.getServerSideProps= async (ctx) => {
      const { format } = require("date-fns");
     return {
           formatted: format(new Date(), "M/d/yy")
     }
}
```
I will concede that the API you're proposing is more powerful. However the point being made here is that there are already methods out there currently that exist to achieve the majority of this API's functionality in peoples projects.


## Data Fetching
- Already possible with relay as mentioned in the video
- Already possible probably through build tools if your routes are structured in a way that can be statically analyzed you can probably use a combination of pre-rendering, examining the data dependencies and "lifting" that into the parent during build time. (No implementation's seem to exist yet, but I feel like NextJS is starting to cause alot of innovation in this space).
- Already possible in an infinite number of other ways as JavaScript is a very dynamic language I've posted a simple implementation below.
```ts
export const Person(data) {
     return <span>{data.name}</span>
}
Person.data = () => api("/api/person")

// and if that Person has a dependency to fetch its data.
export const Person(data) {
     return <span>{data.name}</span>
}
Person.data = (id) => api("/api/person", {body: {id: 1}});
```
Just traverse your React sub-tree from the parent and run all the data methods. Your API is definitely cleaner and I wouldn't recommend to anyone to use the above code, its just there to show that its possible and its definitely possible in other ways as well.

## XSS
- Just going to leave this here as a note for implementers but obviously the second you allow JSX to be sent over the network you're going to allow for user input to be say.... a script tag with dangerouslySetInnerHTML or a iframe with data:uri. Just needs to be considered/mitigated.


One of the reason I loved hooks is that it solved REAL problems for us that were currently preventing scale in our React applications, where-as I feel like for me personally this doesn't solve real problems I'm currently facing in my React projects.

For me personally, I wouldn't trade a fractional increase in performance for the complexity this brings to a project, especially when I have many other levers I can pull before pulling this one.

---

### #13 — @hamedmam — 2020-12-21 20:54

I really liked the bundle size reduction for the code that is rendered on the server, specially when it comes to third-party packages that are not doing a great job in code-splitting and tree-shaking, 
however the data fetching has limited use cases IMO. 
The idea of decoupling backend and client for large scale applications (microservice architecture) will really stop people from thinking to fetch data from components on the server and in the same language (node), I still strongly believe it has it's own use cases for static marketing websites or smaller scale apps.
That being said, I am still impressed with the work, thank you for making web development easier and more accessible everyday.

---

### #14 — @yazaddaruvala — 2020-12-21 20:57

I feel this RFC should discuss the nuances of how deployments will need to be handled. Deployments require two versions of the server side code, and two versions of the client side code to all play nicely together.

It's relatively common to ensure an API is backwards compatible for one or two deployments before cleaning up the old code. However, what does it mean for a Server Component to be backwards compatible?

For example, the heuristics with an API: "adding new fields" is just fine, "removing fields" needs extra care.

What are the heuristics for a Server Component? Currently it seems like a size (height or width), scroll-type, or even theme change will be backwards incompatible.

---

### #15 — @benjamingr — 2020-12-21 21:04

I read the RFC (thank you for working on making this sort of use case easier and more efficient!).

I am very confused by this sort of code:

```js
import db from 'db.server';

function Note({id}) {
  const note = db.notes.get(id);
  return <NoteWithMarkdown note={note} />;
}
```

All the Node APIs are async - so in the above `db.notes.get(id)` returns a promise (or blocks Node.js for every other user using it). How are users supposed to work around this in server components since according to the RFC there are no effects or `async/await`?

I saw [in the video](https://youtu.be/TQQPAU21ZUw?t=830) Lauren mentions a fetch API that is "as if it's synchronous so we don't have to wrap it in an effect" - how does that work?

---

### #16 — @josephsavona — 2020-12-21 21:09

> XSS

@ShanonJackson Thanks for raising this point. We considered security from the start when designing this proposal and the streaming protocol guards against injection attacks. I'll add a note to reflect this.

---

### #17 — @benjamingr — 2020-12-21 21:12

Actually I installed the experimental version of `react-fetch` and I see it's just suspense - it might be beneficial to release an adapter for "generic" Node APIs that throw when the promise is pending.

Interesting.

(As a random nit - you're using `Resolved` to mean `Fulfilled` in the code)

---

### #18 — @Kukkimonsuta — 2020-12-21 21:23

This is interesting concept, however I'm not sure for how large portion of the react community it actually solves any problems. If I understand correctly I can't use this (or I'm limited in using this) when I'm

* not running javascript on server
* using mutable state (ex. mobx)
* using non-serializable state (ex. symbols, classes)
* depend on reference equality


Considering these points I'm very unlikely to ever use it, so let me ask - how pay to play is this? How aware do existing react packages need to be of this existing? Does it affect performance/bundle size even when I'm not using it?

---

### #19 — @benjamingr — 2020-12-21 21:27

> using mutable state (ex. mobx)

Why would that not work?

-----

As a side note, I think it's worth exposing (in a `react-server-components` package or something) the utilities used throughout things like `react-pg` and `react-fetch` like `createRecordFromThenable` and `readRecordValue`.

---

### #20 — @Kukkimonsuta — 2020-12-21 21:35

@benjamingr I may be wrong, but I don't think the server side component can be made observable, so it wouldn't update when property of an object passed in through prop changes. I also believe observability is stripped from object when going through serialization (getters/setter/proxy information is not serializable) so this could break any client components called by the server component as well.

---

### #21 — @josephsavona — 2020-12-21 21:53

@dfabulich (and @benjamingr) With respect to async/await and the data-fetching APIs used here, I've updated the FAQ to [include more context](https://github.com/reactjs/rfcs/blob/2b3ab544f46f74b9035d7768c143dc2efbacedb6/text/0000-server-components.md#why-not-use-asyncawait). I realize that answer is probably a bit frustrating ("ok but why?") but we'd like to keep discussion here focused on the main theme of the proposal. Point taken that we should document this aspect of Suspense. We'll prioritize a follow-up RFC to cover Suspense.

---

### #22 — @Gregoor — 2020-12-21 22:19

> I feel this RFC should discuss the nuances of how deployments will need to be handled. Deployments require two versions of the server side code, and two versions of the client side code to all play nicely together.

I think it would be fair to consider this outside of this scope. My expectation (from what I've read so far) is that implementing bundlers would output something like a manifest from which you can infer whether a chunk is relevant for the server and/or client. Then you'd have a _thing_ in the server which knows how to read that and use ReactDOMServer to render the relevant bits.
Now to get to your point: In that model you'd just need to be able to point the _thing_ towards the different build artifacts depending on, for example, a parameter in the HTTP GET.


___

Thanks React & Data team, exciting stuff!

---

### #23 — @phaleth — 2020-12-21 22:50

Please, rather than demonstrating server components on a TO-DO app that doesn't even require login, consider trying to solve more widespread challenges in your demos. Such as validating an e-mail address on a form, both client and server side. Client side to check formatting quickly and server side to check both formatting and if the entry already does exist in a backend db. Form validation is something that always needs to be done server side because of user trust issues and also client side for non-malicious user friendliness.
Also please, consider making these server components run on any JS environment such as https://github.com/phpv8/v8js and make sure they work on clustered environments and with keep-alive connection. Consider making already rendered server components to be re-usable between different clients. Don't let the same code re-run and components rerender on every request.

---

### #24 — @jimisaacs — 2020-12-21 23:17

Really interested what this would look like in a serverless environment. (react lambda?)

---

### #25 — @SimenB — 2020-12-22 00:54

I'd love to see a section about (unit) testing be added to the FAQ.

I.e. Jest today works without "bundling" code, it will read code from FS and execute it in either a Node based environment or a DOM (via JSDOM) based one depending on user configuration. Is the idea that in order to run tests you'd have to create separate bundles ahead of time based on whether you wanna test the server or client side (or a third bundle which somehow combines the two) or some sort of clever renderer that does the correct thing? Or is the current thinking that people keep writing the same tests they do now, but ensure to only render one side of the "equation" (client or server). Or maybe even some sort of deeper integration to do something that makes it more seamless

---

### #26 — @Daniel15 — 2020-12-22 01:00

> make sure they work on clustered environments

@phaleth the RFC says:

> We are running an experiment with a small number of users on a single page, with encouraging results (already ~30% product code size reduction)

and Facebook probably has one of the largest server clusters in the world 😄 . Anything that's built has to work "at Facebook scale", which includes working in large clustered environments. I don't think a clustered environment would affect much since as far as I know there's no persistent state server-side (the only state is within the context of an individual request). Similarly I think it'd work fine in a "serverless" ("lambda") environment.

---

### #27 — @Jack-Works — 2020-12-22 01:35

It would be nice to support a custom serializer for props. In our codebase, we'll transfer data across JS contexts and "resume" their prototype. I think it will also apply to the Server Components. A class `T` is loaded on both server and client, and the same serializer is configured then it's possible to serialize T from server to the client.

---

### #28 — @yisar — 2020-12-22 02:14

> All Components in peoples projects can either be thought of as 'Isomorphic' if that codebase is using server-side rendering, 

It seems impossible from the current demo, because `useState()` and `useEffect()` will no longer be supported.

I probably took a look. From the overall demo, it seems to be useless, because our components cannot be all server components, No way that bundled with zero, because we need `useState()` and `useEffect()`, these are not available on the server, unless the same as ssr twice water injection, but in that case, why don't we use ssr?

---

### #29 — @chiqui3d — 2020-12-22 03:15

Congratulations and great explanation! This is going to make awesome to generate static pages.

Then I saw several things:

1. I don't see any mention that the server component props come from the parent component server or the `Request `object of Node.js, besides, https://github.com/nodejs/node is not mentioned once
2. The development tools should not show anything about what the server does(This means that React does not store too much information from the server), it would be a security problem if someone installed a React Developer Tools extension and saw everything the server does to exploit it. As they do now with GraphQ, that from the client you send and GraphQL gives you what you want.


Having this system in other server languages such as PHP 👀, would also be impressive to use as my preferred template engine, but we'll have to see the rendering speed to see if it's worth it. For one thing that is not a static page.

---

### #30 — @avindra — 2020-12-22 03:21

For PHP, bridges might be made with [v8js](https://github.com/phpv8/v8js) or webassembly. Also via wasm it should be possible to link other languages like C and Rust.

---

### #31 — @justinkunz — 2020-12-22 04:11

This is great! Only downside is having to maneuver the interactive pieces into separate components. It might be useful to add a built in ClientComponent wrapper into the top level React API that on build could be bundled into its own separate client component. I would see a lot of value in something like this:

``` js
// MyServerComponent.server.js
const serverData = fetch(“http://localhost:4000/data”);

  return (
     <div>
          <h3>{serverData.title}</h3>
          <React.ClientComponent uniqueIdentifier=“my-example”>
              <p>I’m a client component rendered inside a server component</p>
              <button onClick={() => console.log(“clicked!”)}>Click Me</button>
          </React.ClientComponent>
    </div>

)
```

React Bundle on build:

```
.
├── src
│   ├── Foo.js
│   └── Bar.js
│   └── extracted-client-component-my-example.js
```

---

### #32 — @jamesknelson — 2020-12-22 04:35

Congrats on the release of this! There's obviously been a huge amount of work on the design, implementation and presentation.

I really like the idea of rendering per request - like Dan said in the video, it feels a little like the good old days. I do hope that we're not also going back to a situation where every navigation action requires React to contact the server - but it sounds like that's going to depend on how routing is handled. I'm very curious to see more discussion on the research you're doing on this.

I'd also love to hear a story on authentication. The way I see it, authentication information is part of the "request" that the server is rendering - and probably should be handled by the router. However, at non-facebook-scale, authentication is often handled by client-side APIs provided by the likes of Auth0, Google or AWS. If routing happens on the client, this is easy enough to integrate. But with server components, routing needs to happen on the server. And while auth APIs do provide ways to generate separate tokens for use on the server, connecting it all up in such a way that you can consistently get the same result from a `fetch()` called on the client and the server takes some work.

Another comment as a non-facebook-scale developer is that I want a mechanism to make multiple IO calls in parallel, similar to Promise.all, but for Suspense. From what I understand, the current idea is that because IO is running on the server, each IO call should have a low cost, and thus the waterfall effect should be insignificant. However for smaller companies, the reality is often that to render a single page, we'll need to access multiple data sources across different regions .

As an example, some content may be accessed via a headless CMS API hosted in the Midwest, while other data may be hosted on a Heroku Postgres db (which only provides non-specific "us" and "eu" regions that could be located anywhere). If you want to check that the auth token hasn't been invalidated, then that's another check to probably another region. And there's no guarantee that the web server orchestrating all these requests will be anywhere near *any* of these services. While a Promise.all equivalent won't solve this completely, it'd certainly make it a little less painful.

One last thing I'd like to see more discussion on is how data fetched on the server can be automatically passed to the client to use as the initial value for a cache, without needing to manually extract it on each request and pass it as a prop. For example, say you make a GraphQL query in a server component, and you want to then start a subscription to that same query on the client. How do you do this cleanly, without making an unnecessary request on the client, and without needing to duplicate code across the server and client components?

---

On a different note, while I can see that this will certainly simplify application code in a lot of cases, I'm a little worried that this will cause a split in the ecosystem similar to the python 2/python 3 days. At the risk of stating the obvious, *server components require a server*. React, at least until now, hasn't required a server. Any improvements in DX that server components provide will only be available to people who are willing and able to deploy a React server. Many legacy apps won't be able to do this, while many others will choose not to - as server components will also involve financial costs that are absent in client-rendered components. In effect, we're going to end up with two very different tools with two very different ways of doing things. I'm worried that it'll be a little confusing if they're both called "React".

This really does look pretty neat though. I'm looking forward to giving it a try.

---

### #33 — @itsjoekent — 2020-12-22 06:28

Throwing my two cents in! It seems like Server Components relies on the theory that rendering components on the server will always be "faster", but it is glossing over how much "work" that entails to be true at scale.

Introducing web server(s) that might get hit with anywhere from 5-10 "component requests" per page on average, each of which might be requiring database queries or third-party API lookups, is only going to work if you really invest in an infrastructure that keeps all of that data close to this "component server", constantly up to date, and automatically scalable for any sudden traffic spike (because if the component server gets overwhelmed... your frontend is gonna be stuck loading forever). And of course there would have to be a great deal of thought put into deployment/rollback synchronization, caching, etc. of this component server to ensure the deployed frontend assets always match the server, otherwise your client-side hydration would likely fail.

Maybe Facebook doesn't have to worry as much about introducing these infrastructure architecture challenges, because there is undoubtedly an army of engineers on standby to solve that. But many of us have to think critically about budgeting time to maintain API's with all of those same reliability & scalability requirements, but now we'd have to add _another_ critical system to our infrastructure, just to make a handful of UI components maybe render a few milliseconds faster.

It just doesn't sit right with me that a UI library would introduce all of these infrastructure requirements to use a core feature (_it is weird we are even talking about infrastructure in the React repository!_), especially given that there are _a lot_ of improvements that could be made to the existing process of server-side rendering, something that almost all of us depend on, and frameworks are already doing some [really interesting work around this](https://nextjs.org/blog/next-9-3#next-gen-static-site-generation-ssg-support).

---

### #34 — @jansivans — 2020-12-22 09:33

I have created similar working solution some time ago.
You program components which are fully server-side inside your browser using React-like syntax.
You can use anything nodejs has (`fs`, databases, etc.).
It also stores state (like you can see in demo `counter` variable).
Browser only receives JSON-structure of what it should render and sends actions to server via websockets.
It also has lifecycle - component is created on server in separate process until user navigates away from it.
If you are interested, I can share some info in more detail.

https://user-images.githubusercontent.com/5667073/102872479-66ebde00-4448-11eb-9d9a-7e767a2cb4b2.mp4

On the left side you see a browser with code editor + component previewer.
On the right side you see opened VS Code with the file which is saved by a component.

---

### #35 — @aralroca — 2020-12-22 10:14

I understand that it is similar to using the hack to avoid hydration, but that it also avoids downloading the JS involved, that's awesome! Moreover, it makes automatic dynamic imports... It looks very good, but I wonder if this will have a downside of doing the imports automatically... 

As I see, the initial loading of the example downloads 6 `.js` files. They are small but there are 6. What happens in big applications where there is a lot of content with a big scroll? Is downloading only the components that are visible to the viewport and it downloads the rest progressively while scrolling? Or is it something that we will have to continue controlling?

Even if HTTP 2.0 is used, I understand that more than 20 req per page to download all the client components could be harmful, and IMO it should prioritize those components that are visible in the viewport.

---

### #36 — @xyy94813 — 2020-12-22 10:39

How about Server Component with auth?

Server Component with logined state? JWT? Session?
Should I handle permission before render Server Component?
If Server Component require some sensitive data?

React Server Component is awesome.
But, we still need time to get a best practice.

---

### #37 — @SystemParadox — 2020-12-22 12:13

This looks exciting. Perhaps I've missed something, but is it not possible for server-side components to subscribe to data and send subsequent changes to the client? This seems like a glaring omission, particularly for dashboard monitoring type screens.

We've been working on our own server components system for the past couple of years but ours is quite different to this. Our system allows any component to be given a corresponding server-side portion that deals with data fetching. When the component is mounted on the client-side it subscribes to the server-side which effectively "mounts" the server-side (although it's only for data, it doesn't do any rendering), which in-turn allows the server-side to subscribe to data that might change and send those change events down to the client. It's effectively an extra layer of state, although we don't allow the client to make changes to it directly, and it's provided through a context object on the client.

The server-side portion can also declare actions that can be called by the client-side, but they can only run if the server-side component was allowed to mount in the first place, which makes permission checking so much simpler.

React clearly needs something to make it easier to fetch data directly on the server and this proposal looks like it will help with the initial rendering case, but it doesn't seem to address ongoing subscriptions and I would be interested to hear what the React team thinks of our approach to this.

We're generally working on 'live' multi-user dashboard type applications so perhaps our use case is very different. We don't currently have a way for a component to load some data from the server-side portion without keeping an active server-side subscription, which isn't really appropriate for a more traditional website where you just want to load the page once for the user to read. Although I'm sure it would be easy for us to do this.

---

### #38 — @darrenc-alcumus — 2020-12-22 12:28

I must admit, after reading and watching the video - I fail to see how this isn't just a form of view data wrapping the actual requested data, and do not see what additionally it provides that couldn't be done in a resolver or standard api. The example of reducing bundle size equally applies to doing date formatting server side and optionally requesting it via a graphql call or such.

---

### #39 — @Raxvis — 2020-12-22 17:52

Seeing as you are still making trips to the server, I fail to see how Server Components will be any faster overall.

If you have three components and two of those are server components, wouldn't that require two trips?  How is that faster than two api calls?

I can understand the performance if they are all nested under a single top Server Component, which is the only trip to the server but this seems like a least useful implementation. 

### Example
*non-performant server side components*
```js
import SpotifyArtist from './SpotifyArtist.client';
import SpotifyDiscography from './SpotifyDiscography.server';
import SpotifyAlbums from './SpotifyAlbums.server';
import SpotifyArtistInfo from './SpotifyArtistInfo.server';

<SpotifyArtist>
    <SpotifyDiscography artistId={artistId} />
    <SpotifyAlbums artistId={artistId} />
    <SpotifyArtistInfo artistId={artistId} />
</SpotifyArtist>
```

*performant server side components*
```js
import SpotifyArtist from './SpotifyArtist.server';
import SpotifyDiscography from './SpotifyDiscography.server';
import SpotifyAlbums from './SpotifyAlbums.server';
import SpotifyArtistInfo from './SpotifyArtistInfo.server';

<SpotifyArtist artistId={artistId}>
    <SpotifyDiscography artistId={artistId} />
    <SpotifyAlbums artistId={artistId} />
    <SpotifyArtistInfo artistId={artistId} />
</SpotifyArtist>
```

Am I missing something or not understanding something with this proposal?

Wouldn't a better method be a way to chain all the api fetching method together so that all three calls are made at once (parallel)  and then resolved all together?  That way you get the best of all three world (fast, good, cheap).  Something to how dataloader works but with api calls? This could even be tied into Suspense, but you get the ability to wrap each Component in Suspense and your UI feel like a single page while if you need to update a single component down the line, only it would be  held in Suspense.

---

### #40 — @Mathspy — 2020-12-22 18:01

> Am I missing something or not understanding something with this proposal?

@Prefinem as the proposal stands it’s not even possible to use client side components if the top level component is a client side one as client side components can never render server side ones, at least not directly. So it’ll always be the “performant” case

---

### #41 — @mlrawlings — 2020-12-22 18:13

As @cangoektas [just mentioned in a now collapsed comment](https://github.com/reactjs/rfcs/pull/188#discussion_r547319694), "Server Components are praised as a solution to the waterfall problem when they would only (as of right now) minimize the symptoms of it."

Waterfalls haven't been eliminated, they've just been moved to the server.  For something like the demo, where the database is running on the same machine and you're making simple queries against tables with 5 rows, yeah, it's no longer a big deal that there's waterfalls.  

But the further your frontend server moves from your backend API servers, the more pronounced network latency and therefore the waterfall effect is going to be.  For Facebook, where these servers live in the same data centers, the network time is likely much less pronounced.  But if you have APIs whose latency is primarily due to computation time or you're running your frontend server on the edge but still have centralized backend APIs, I doubt this is a fully solved issue.  I'm not saying moving the waterfall to the server is without benefits.  I _am_ saying ["No Waterfalls"](https://github.com/reactjs/rfcs/blob/ce4e353d4edbea2f05e1a2154b79f0e559d65748/text/0000-server-components.md#no-waterfalls) is a bit disingenuous.

---

### #42 — @Raxvis — 2020-12-22 18:16

> @Prefinem as the proposal stands it’s not even possible to use client side components if the top level component is a client side one as client side components can never render server side ones, at least not directly. So it’ll always be the “performant” case

Then isn't this just SSR?  I assume that once an app has loaded on the client, there will be components if they are loaded, they will make the trip to the server (hence server components).  From the demo, when a note is selected, it loads the note in the app without doing a full page request. (at least this was my thought when I watched it)

---

### #43 — @gaearon — 2020-12-22 18:21

>All the Node APIs are async - so in the above db.notes.get(id) returns a promise (or blocks Node.js for every other user using it). How are users supposed to work around this in server components since according to the RFC there are no effects or async/await?

All of the calls in the demo are asynchronous. We model reads as reads from the cache, and if the entry is missing in the cache, we throw and retry when it's fetched. We'll describe this mechanism and the reasoning behind it in a future separate RFC.

>Another comment as a non-facebook-scale developer is that I want a mechanism to make multiple IO calls in parallel, similar to Promise.all, but for Suspense. From what I understand, the current idea is that because IO is running on the server, each IO call should have a low cost, and thus the waterfall effect should be insignificant. However for smaller companies, the reality is often that to render a single page, we'll need to access multiple data sources across different regions .

Please note that calls in sibling components are parallelized with Suspense. However, for server Parent-Child waterfalls, when those become a problem, there would be an ability to "preload" requests early as an additional opt-in optimization.

You could argue that this means waterfalls aren't a problem on the client either, but practically speaking, even if server waterfalls are not ideal, client-server waterfalls are outright disastrous. Servers also offer more leverage to fix waterfalls automatically, such as with [DataLoader](https://github.com/graphql/dataloader)-like caching abstractions.

> However the point being made here is that there are already methods out there currently that exist to achieve the majority of this API's functionality in peoples projects.

Indeed, none of these problems is unsolvable in isolation. But we felt that there was no cohesive solution that solves them together in a way that feels idiomatic to React, in a way that scales up and down, and in a way that doesn't require specialized knowledge. This proposal is a refinement and a remix of different ideas from different sources.

>The development tools should not show anything about what the server does(This means that React does not store too much information from the server), it would be a security problem if someone installed a React Developer Tools extension and saw everything the server does to exploit it. As they do now with GraphQ, that from the client you send and GraphQL gives you what you want.

We were only referring to the development environment — where the code would likely run in a Worker rather than a Server. It should not be possible to access a production environment in this way.

>I was a little confused in the demo... why can't you achieve serialization of functions by just using JSON.stringify() and comparing the implementation?

Functions close over other values, so you can't transport code this way unless you literally transfer the JS bundle, which puts us back at where we are today.

>Introducing web server(s) that might get hit with anywhere from 5-10 "component requests" per page on average,

To be clear, there are no separate "component requests". We request the whole Server tree — one request per navigation, with a streamed response. For refetches, we'd be able to request a refetch of either the whole tree (similar to a page reload) or a subset (e.g. a sidebar), with refetch granularity determined by the developer.

>If you have three components and two of those are server components, wouldn't that require two trips? How is that faster than two api calls?

Same, you wouldn't have two responses for the same reason that when you request a page from Django and it uses two templates, you still get only one response. They are composed on the server.

>frameworks are already doing some really interesting work around this.

This proposal was designed in collaboration with the framework you link to. :-) There's undoubtedly good work there, and we want to provide the missing building pieces to make it more powerful. But nothing stops you from keeping to use the existing techniques if they fully satisfy you.

>As I see, the initial loading of the example downloads 6 .js files. They are small but there are 6. What happens in big applications where there is a lot of content with a big scroll? Is downloading only the components that are visible to the viewport and it downloads the rest progressively while scrolling? Or is it something that we will have to continue controlling?

I think you're misreading the example and seeing the _sourcemaps_ — i.e. the original files. There are way fewer _bundles_ than that. Still, the work to determine an optimal bundling strategy and heuristics will be a part of productionizing the bundler plugin. The actual granularity is not inherent to the approach — we can make it as coarse or as granular as needed.

>but is it not possible for server-side components to subscribe to data and send subsequent changes to the client? 

Server Components are not stateful by design — they don't "run" on the server. They are much more similar to a classic request-response model. You can still use Client Components to subscribe to streams of data.

---

### #44 — @Daniel15 — 2020-12-22 18:22

> But the further your frontend server moves from your backend API servers, the more pronounced network latency and therefore the waterfall effect is going to be. 

@mlrawlings Servers tend to have better connections though, so a waterfall on the server-side isn't as bad as a waterfall on the client-side. Servers typically have very fast connections - 10 Gb/s is becoming more common, but most servers are at least 1 Gb/s now. Data center internet connections are higher quality with a lower contention ratio than residential connections (which can often be 3G or 4G networks with high packet loss).

It's also easier to optimize the server-side. For example, if the database is in a different location to the web server, you could have a Memcache server in the same location as the web server to cache hot queries. Similarly, it's easier to batch similar queries together on the backend, which is what we do at Facebook (if there's multiple concurrent requests to load data from the "users" table, it'll combine them all into one query).

I agree that the heading "No Waterfalls" is not ideal though. Maybe it should be "No Client-Side Waterfalls"?

---

### #45 — @itsjoekent — 2020-12-22 19:06

@gaearon I appreciate the response! The core point I was trying to raise is, the level of work involved to successfully leverage server components is quite high, and the pitch of server components obfuscates that point. 

To be clear: I'm not making an argument that Server Components should _never_ be implemented, I certainly think with more refinement the API could land somewhere quite useful & neat. But I do hope this doesn't reprioritize the roadmap away from fully implementing partial rehydration and other SSR performance improvements that could have immediate wins for everyone already relying on SSR & an existing architecture/codebase they need to maintain.

---

### #46 — @aliraza-noon — 2020-12-22 19:58

this definitely looks interesting, similar approaches have been taken by other platforms like Phoenix LiveView https://github.com/phoenixframework/phoenix_live_view, but they target native html instead of react or any js framework

---

### #47 — @SawyerHood — 2020-12-22 20:58

This is super exciting and the RFC is really well put together. Did the team consider allowing for server components to be nested inside of client components? I understand why this isn't allowed because it would be a pretty big foot gun that could reintroduce waterfalls on the client side again. I can think of a few really useful examples of wanting to do this, ex: you might want to render a server component inside of a modal that only opens when the user takes a certain action. 

Is the suggested way to do something like this have a server component that passes the modal to a client component and add a query param like `?modal=share` to the route to signal that a modal should be rendered?

---

### #48 — @ricokahler — 2020-12-22 21:52

Overall, I really like server components. I think it's wonderful addition to the React model, and it's something novel (at least to me) that fundamentally changes React to more than just a CSR lib.

There were previous comments that discussed some hesitancy to this model because of this but my opinion is that that's okay — what they're trying to do requires this careful orchestration that's not possible without some of the React core model updates. They'll release some webpack plugins, some babel plugins, and some new client-side APIs but what I always appreciate is that these new tools are opt-in and current React is still React.

Before I get into some of my other comments, I just wanted to say I really appreciate that you're working with the Next.js team to bring this to life. Next.js already gives our app a lot of performance benefits by utilizing pre-rendered SSRed pages (i.e. the "jamstack") and working with them should create a well-rounded, performant vertical that's relatively cheap to host if paired with pre-rendering/the jamstack.

Next.js has already made us comfortable making similar tradeoffs between what's client-side rendered vs what's server-side rendered, and what's dynamic vs what's static. Adding another choice between server component vs client component should pair well.

To talk more on the Jamstack, I can already see a future that combines pre-rendering with server components. During a build, Next.js could pre-render all server components and then cache them on the edge for effectively zero runtime on the server too lol

To repeat my first point, this all requires careful orchestration and infrastructure so, Next.js paired with Vercel is kind of the perfect pairing of infrastructure, bundler, and framework to make it possible (though admittedly kind of monopolistic).

---

I have ~2~ 3 feature requests/concerns

## Reuse more work from SSR

I apologize if this is already the case but my impression was that the current implementation does not behave like this.

> **Does this replace SSR?**
>
> No, they’re complementary. SSR is primarily a technique to quickly display a non-interactive version of client components. You still need to pay the cost of downloading, parsing, and executing those Client Components after the initial HTML is loaded.
>
>
> You can combine Server Components and SSR, where Server Components render first, with Client Components rendering into HTML for fast non-interactive display while they are hydrated. When combined in this way you still get fast startup, but you also dramatically reduce the amount of JS that needs to be downloaded on the client.

> **Why don’t you just use HTML instead of a custom protocol?**
>
> We do want to use streaming HTML for the initial render, but the custom protocol lets us transfer data (component props), and reconcile trees so that the client state as well as DOM focus/scroll/state doesn’t get blown away.

Reading the RFC and the above, it does not seem like it's a goal to re-use the work done from SSR when trying to hydrate server components. Maybe this is complicated because of some constraints with reconciliation, but I think there's an opportunity missed if this goes without.

Let me clarify with an example where the traditional SSR + CSR hydration model falls short:

When writing a blog post component with Next.js today (as an example of typical SSR + CSR hydration), the client first downloads the fully server-rendered version of the blog post as HTML. This HTML contains all the content of the blog post in already in the HTML yet the browser downloads this content again in the JS when it goes to download the code to re-hydrate the server rendered version.

Since server components are non-interactive, it seems like it should be possible to re-use the work done in SSR so that that content only needs to be downloaded once. This is where I think it make sense to use some variant of the "custom protocol" that is also HTML so that SSR work can be re-used during hydration. The logic could be "check DOM if server component is already rendered, otherwise make network request to server".

My assumptions might be wrong here but that's what I read into when reading "custom protocol". Any clarification on this would be greatly appreciated!

## Ensure the use case of pre-rendered Server Components is covered (Jamstack)

As I said above, I'm glad y'all are working with the Next.js team to bring this to life because Next has embraced the Jamstack philosophy of "pre-render at build time".

I think it's really important this case is covered because it greatly reduces the cost of infrastructure to use server components, and for many uses cases (ecommerce sites, blogs, content-based sites, etc), there is no need for personalized pre-request responses anyway.

I'm sure the Next team will have more to say for this topic but I just want to bring this up as a major use case. For those of us who are building mostly static Jamstack websites, server components should be a big win with no significant infrastructure cost.

## Allow no-op useEffects in Server Components (e.g. for shared components)

> **Sharing Code Between Server and Client**
>
> ❌ May not use rendering lifecycle hooks such as effects.

This kind of took me by surprise. I understand that they cannot work but I don't yet fully understand why I can't put in a `useEffect` that will simply no-op in the context of a server component yet work in the context of a client component.

Maybe I'm just coming from the perspective of being used to writing SSR and CSR compatible components, but I'd love any help explaining why it won't work or why it just doesn't make sense.

---

### #49 — @ShanonJackson — 2020-12-22 23:09

- The reason we loved hooks is it allowed us to SIMPLIFY a lot of our stateful logic and scale through reusability. There was a tradeoff with abstraction where now we have to think about closures and dependency arrays but this trade-off was judged to be worth it.
- The reason we loved Suspense is it allowed us to SIMPLIFY a lot of logic related to data fetching and spinners allowing us to write "synchronous" looking code, the same way async/await allows us to write "synchronous" looking code. Again There was a tradeoff with abstraction to include throwing promises in your data fetching logic and thinking where to position your Suspense components.
- The reason I don't like this is that it doesn't "simplify" for the consumer, it makes things significantly more complex for the sake of a tiny performance gain. I would rather optimize my bundle size and critical network path through other methods before resorting to server/client components. If you're adding abstraction the trade off must be worth it and for me in this case its not.

@gaearon  I agree that the things listed in my earlier post here AREN"T idiomatic React, however if the benchmark we're setting is for a solution is to be idiomatic React this RFC is also not idiomatic React. It's trying to mold the definition of idiomatic React to include differentiating components by render environment.


Here's some more thoughts just generally about the direction being taken here and why I like it, but just not this RFC

Should React really be shifting their focus from innovating in the client to innovating in the server? Does this make sense as a frontend framework? (I think yes, but not for this feature, but again the community should have a say).

I do however think there is a case for 'no' it shouldn't be innovating on the server, not everyone uses SSR and not everyone has a NodeJS backend. I think only a small fraction of the community actually uses this functionality and a micro-fraction of that fraction has the same problems Spotify and Facebook do at scale. I do not think the problems of a small minority should be driving the direction of the library.

---

### #50 — @s4san — 2020-12-23 01:46

How would server components support cancellation and race conditions between server tree re-fetches? Would there be a mechanism to invalidate and ignore stale responses (on client) and to stop processing existing renders (on server) based on the recency of incoming requests? (E.g. A find-as-you-type component powered by server side components)

Promise based APIs are notoriously bad at this and it would be nice if developers didn't have to worry about Signals and AbortControllers for each server side component they develop.

---

### #51 — @yisar — 2020-12-23 01:47

> Server Components are not stateful by design — they don't "run" on the server. They are much more similar to a classic request-response model. You can still use Client Components to subscribe to streams of data.

I think this is the reason why React has become a framework. In fact, it is impossible for all components to be stateless, so 0 bundle size is also impossible.


I think the mental burden of this feature (stateless, no runtime) are very heavy. In the future, users should not only care about class components, hooks components, but also server components. React has become more and more frameworked, which is not a good thing. At least for me.

---

### #52 — @thomas-brex — 2020-12-23 04:12

The example in the video mentioned moving the `date-fns` dependency to the server as a benefit of server components.

Wouldn't this actually be a pitfall since the Date  API depends on local timezones of the machine and this code would now be executing on the server (using that machines timezone)? 

Some of the limitations of this pattern are outlined, such as not using state or DOM functions, however it seems that, as occurred in the example of the announcement, it will be very easy to let hard-to-find "bugs" be introduced when writing code for server vs. client components.

---

### #53 — @Drakota — 2020-12-23 08:20

Wow! This looks very cool. Really excited to try this out.
@gaearon you briefly mentioned using Server Components with GraphQL, would it be possible to have some examples to see how this would look like when paired together and how to use those two technologies optimally?

---

### #54 — @mallchel — 2020-12-23 09:19

How about to use server components in the future in the React Native?

---

### #55 — @darrenc-alcumus — 2020-12-23 11:30

Further to my previous thoughts... isn't this just a new "content-type" for a returned API call "text/react-component" - as essentially all we are doing is reformatting the API call that we make. We could then fetch these / stream or whatever we need and treat them as data.

---

### #56 — @gaearon — 2020-12-23 15:48

>But I do hope this doesn't reprioritize the roadmap away from fully implementing partial rehydration and other SSR performance improvements that could have immediate wins for everyone already relying on SSR & an existing architecture/codebase they need to maintain.

I don't quite understand what you mean by "partial rehydration" here so it would help to clarify your expectations about this concept. Generally saying, we've already implemented the kind of SSR improvements that are possible in the React model without breaking its guarantees. In Concurrent Mode, we can:

- Start hydrating parents before all the code for children has finished loading.
  - Try our best to preserve unhydrated HTML even if the relevant code isn't loaded yet.
- Hydrate in chunks instead of stalling the main thread.
- Prioritize hydrating the part that the user has started interacting with.
- Replay some of the events that happened before full hydration.

But there is a limit to what we can do here. So Server Components is about taking a bigger step forward, with async data fetching, automatic code splitting, and so on. They build on top of SSR improvements, not replace them.

>Did the team consider allowing for server components to be nested inside of client components? I understand why this isn't allowed because it would be a pretty big foot gun that could reintroduce waterfalls on the client side again. I can think of a few really useful examples of wanting to do this, ex: you might want to render a server component inside of a modal that only opens when the user takes a certain action

Note you can nest SC into CC as long as the _nesting itself_ happens in another SC above it. But generally saying, there is always some kind of an "entry point" into the SC world, and you're right in some cases it makes sense for this entry point to be "lazy". We shouldn't make this too easy like you said, but technically this capability will definitely exist, including for the use case you mention. Although that use case might also have a more idiomatic solution on the server side.

>Is the suggested way to do something like this have a server component that passes the modal to a client component and add a query param like ?modal=share to the route to signal that a modal should be rendered?

Yes, something like this might work. Routing is still an open research area, and lazy interfaces like tooltips, modals, etc, will be a part of that research. We need to get Server Context support in first before exploring this.

>To talk more on the Jamstack, I can already see a future that combines pre-rendering with server components. 

Yes, this is definitely something we want to support.

>Since server components are non-interactive, it seems like it should be possible to re-use the work done in SSR so that that content only needs to be downloaded once. This is where I think it make sense to use some variant of the "custom protocol" that is also HTML so that SSR work can be re-used during hydration. The logic could be "check DOM if server component is already rendered, otherwise make network request to server".

The intention is for the first render to never need another request to the server. The HTML streaming renderer would embed the JSON chunks in the HTML response so that we both get the fast non-interactive render, and then get to interactivity as soon as possible. There is still some duplication between HTML and JSON, but note how this is different from today's solutions that serialize the whole server-side cache content — because we only serialize what's *actually on the screen*. Additionally, we can be clever about the encoding and avoid repeating text — e.g. the JSON could have special markers like `"$H"` that tell React to reuse the HTML text node's value. Since we know it won't change until next navigation, and it's opaque to the actual JS code anyway.

>Ensure the use case of pre-rendered Server Components is covered (Jamstack)

Yes, running Server Components at the build time is part of the paradigm.

>This kind of took me by surprise. I understand that they cannot work but I don't yet fully understand why I can't put in a useEffect that will simply no-op in the context of a server component yet work in the context of a client component.

In Client Component SSR, the initial render result is just a non-interactive "snapshot" of the initial visual state. So it makes sense that effects are noops there. But for Server Components, they're never shipped to the client at all, so the effect would never run. If you want that effect, move it into a Client Component, which you'd import from a Server Component. Then for the first render (traditional SSR) you'd see a mix of both SC + initial render of CC (which may have noop effects).

>The reason I don't like this is that it doesn't "simplify" for the consumer, it makes things significantly more complex for the sake of a tiny performance gain. 

We don't expect the performance gain to be "tiny" at all, but you're welcome to ignore this and still do data fetching on the client side. Suspense works in both places, although it's more powerful on the server.

>I agree that the things listed in my earlier post here AREN"T idiomatic React, however if the benchmark we're setting is for a solution is to be idiomatic React this RFC is also not idiomatic React. It's trying to mold the definition of idiomatic React to include differentiating components by render environment.

This is obviously subjective but I find the proposed solution the most idiomatic solution for "data fetching on the server side" (https://github.com/facebook/react/issues/1739) than anything else I've seen before. I'm curious if you don't consider this a worthwhile problem at all, or if you have a more idiomatic solution to compare with.

>Should React really be shifting their focus from innovating in the client to innovating in the server? Does this make sense as a frontend framework? (I think yes, but not for this feature, but again the community should have a say).

I'd phrase it differently. React isn't shifting focus *from* the client — today all of React is client! It's just that the server has been vastly underdeveloped, and we want to have parity. Then you get to choose the tradeoff for your app.

>I think only a small fraction of the community actually uses this functionality 

We can say with confidence that this isn't correct. E.g. our recent community survey has shown ~30% respondents use Next.js, which has server rendering. npm downloads tell the same story. SSR is important to the ecosystem, although there will definitely always be apps that don't use it, and we want to support them well too.

> I do not think the problems of a small minority should be driving the direction of the library.

Again, we don't agree with this framing and we consider excessive bundle sizes, long stalls during client rendering, and network waterfalls very common problems across the ecosystem, _especially_ at smaller companies that don't have the kinds of resources Facebook or other companies might have to invest into solutions to perf problems. Like I emphasized in the talk, the reason we're excited about Server Components is because we genuinely believe they will benefit the vast majority — big and small, professional and hobbyist. 30% (which is Next.js alone) is already a lot of websites, but many have told us they don't use SSR precisely because there hasn't been an easy data fetching solution that feels "Reacty". And SSR alone can't solve most of these problems (e.g. granular code-splitting or keep code server-only).

>How would server components support cancellation and race conditions between server tree re-fetches? Would there be a mechanism to invalidate and ignore stale responses (on client) and to stop processing existing renders (on server) based on the recency of incoming requests? (E.g. A find-as-you-type component powered by server side components)

Race conditions are handled by the Suspense paradigm — you read from cache during render synchronously, so you can't get the "wrong" result. Cancellation is more tricky. We'll have a built-in AbortSignal that's tied to fetches under the hood, but we might have to not be as aggressive about cancellation as some other solutions due to technical constraints. However, keep in mind that the responses fill the cache so they're not entirely useless either.

>In fact, it is impossible for all components to be stateless, so 0 bundle size is also impossible.

Pretty much the whole point of the proposal is that you can interleave Server and Client components as much as you want. Your app's total bundle size is quite unlikely to be zero, but you can be confident that Server components don't contribute to it. Again, you don't have to use them if you find no need for them, but in our experience a lot of components just want to grab or transform some data, and actually don't need state.

>In the future, users should not only care about class components, hooks components, but also server components.

By this point it's pretty clear that the React community has embraced Hooks, so we expect classes to start fading away and only show up in legacy code (which we'll keep supporting).

>The example in the video mentioned moving the date-fns dependency to the server as a benefit of server components. Wouldn't this actually be a pitfall since the Date API depends on local timezones of the machine and this code would now be executing on the server (using that machines timezone)?

Indeed, and this is another example of how we can make product-specific choices. E.g. if this is a problem or if we want relative dates, we can make our `<Timestamp>` a Client component without changing other code. It lets you make those decisions and then revisit them on a per-component basis.

>you briefly mentioned using Server Components with GraphQL, would it be possible to have some examples to see how this would look like when paired together and how to use those two technologies optimally?

You can imagine it similar to this:

```js
function Post({ id }) {
  const post = readQuery(/* your graphql */, { id })
  // ...
}
```

There's not much more to it.

>How about to use server components in the future in the React Native?

We've investigated an initial proof of concept and will likely come back to it, but for the initial rollout we're focused on the web.

>Further to my previous thoughts... isn't this just a new "content-type" for a returned API call "text/react-component" - as essentially all we are doing is reformatting the API call that we make. We could then fetch these / stream or whatever we need and treat them as data.

Yes, you can look at it this way.

---

### #57 — @flybayer — 2020-12-23 19:16

Exciting proposal! Good work everyone!

My only request is please use a serializer like [`superjson`](https://github.com/blitz-js/superjson) which supports serialization for `Date`, `undefined`, `BigInt`, `Map`, `Set`, etc in both directions. [`devalue`](https://github.com/Rich-Harris/devalue) is another option but is only safe for server to client, not client to server.

---

### #58 — @Fouzyyyy — 2020-12-23 19:43

What an exciting proposal! This will introduce new gates of improvements at many levels, nevertheless, I wonder the following things:

1. **Security:** for each http request (even if the domain is localhost) the server components will be performing, what if there is an access token needed? What if there is an authentication and authorisation needed, should the server components authenticate themselves first, and ask for an access token to be authorised to access some data resources?
2. **Performance:** could we cache the server render result of a given server component when the input is the same?
3. **Maintenance costs :** if the server that is responsible for the rendering of our server components is no longer reachable for some reason (say DDOS attack), does this mean that we will have to handle a new type of errors, errors of type: component currently not available? And could this be properly tested ?


Reiterating my feels toward this feature, this is really exciting and possibly opening new ways of thinking in react 🥳

---

### #59 — @cassiozen — 2020-12-23 21:12

Are optimistic updates/rollbacks something that this proposals plans to tackle on or leave to userland solutions?

---

### #60 — @Ephem — 2020-12-23 23:42

Fantastic work on this, really feels like a neat solution to a whole bunch of things and the missing piece to the puzzle. Cudos for a really well written RFC and great presentation and demo too!

I want to highlight and expand on this from @jamesknelson:

> One last thing I'd like to see more discussion on is how data fetched on the server can be automatically passed to the client to use as the initial value for a cache, without needing to manually extract it on each request and pass it as a prop.

I'd like this too, but not just for initial value but updating it on refetches too. Many data fetching libraries populate some kind of external cache so that you can read from that in many parts of an application without having to pass props down. It is likely that both server and client components will want to use the same data, so those solutions will still be important in many apps. Hydrating that cache with data passed from the server is currently tricky in all SSR-metaframeworks because it technically needs to happen before the render to avoid mismatches, but no such opportunity is provided, and it seems like the Server/Client-components boundary would have the same challenge?

Many workarounds today involve just writing to the cache in render which isn't great. React Context is kind of unique here since you can "add stuff" to it in render safely with context providers, but writing to an external cache is not safe. Feels like a point of contention with existing libraries worth investigating more even if it eventually just ends up in a documented recommended approach?

---

### #61 — @wood1986 — 2020-12-24 08:52

Here is my feedback. I am not super excited when comparing with the react hooks introduction. I personally think this is not a right direction. I will use above the fold or below the fold to justify server components approach.

If I need to speed up the components which are above the fold, the existing sever side rendering approaches with the store initialization has already solved client side's waterfall issue and delivered the fastest and best experience to users. So I will not use/change to use server components handle the components which are above the fold.

I can see server components **might** be able to speed up the lazy loading components which are below the fold with the data fetching afterwards. Without server components, I still can increase threshold in order to load the components and fetch the data earlier even if they are still below the fold. Because of that, I will not use/change to use server components either.

Both relay + graphql and server components encourages us to have some server work in order to speed up our app. If I need to have some server work, why do not invest relay + graphql as the long term solution at the very beginning. So my question is will the pattern for server components help us to move relay + graphql easily when I need? If the answer is no, I will not consider the server components approach at least for me. Other than that, I want to know the difference between server components approach and relay + graphql in term of the amount of effort to setup the same infrastructure.

---

### #62 — @raix — 2020-12-24 09:19

First off I like the idea of minimizing/loosening the contract surface between the browser and server.

Questions
* Is this new "jsxon" format / server component format going to be react / javascript only?
* How are breaking changes going to be handled, eg. breaking changes in server component contract?

---

### #63 — @behnammodi — 2020-12-24 11:32

I have a suggestion for the name :)

Cloud Component instead of Server Component

I imagine about Cloud services in future we'll have a new  type of service called CAAS (Component as a Service)

---

### #64 — @brendonco — 2020-12-24 15:46

I think SC will help us decide whether component reside in Server or Client. Also reduce bundle size in client. Especially when you have 4MB library that your app is depending on. The challenge is how to maintain the state e.g. in Redux when your dealing with Route or Micro Frontend

---

### #65 — @stefee — 2020-12-24 18:55

I like this a lot!

---

### #66 — @yisar — 2020-12-25 02:43

I have an idea :

Before we did SSR of client component, we needed secondary hydration and injected events and lifecycles.

However, in the future, we only do SSR of server component, so we do not need secondary hydration.

This will be more pure. This is also the only benefit I can see from the server component, because the loss is huge - let react become a framework.

---

### #67 — @poteto — 2020-12-25 19:23

I wanted to address some feedback on Twitter, but it's a long response so I figured it would be better to post the reply here.

> This doesn't solve the waterfall problem, it just makes it less noticeable.

A prior version of our RFC didn't describe this accurately, and we've since [corrected it](https://github.com/reactjs/rfcs/blob/9732e1a9bd60fa5fe00c6be2fa4fcf35f316ac99/text/0000-server-components.md#no-client-server-waterfalls). It'd be more appropriate to say that React Server Components help solve client -> server waterfalls, but server -> server waterfalls may still exist. But it's also true to say that server waterfalls might not be as big of a problem. And that there are proven ways of solving them on the server that are difficult to replicate on the client.

> Bundle size might be reduced, but that doesn't mean that *total data used* is reduced as well. This could impact old/low-speed devices negatively.

Large bundle sizes means more JavaScript to download, parse, and execute. On low end devices this is a huge problem, because they don't have as much [compute power](https://pbs.twimg.com/media/EkzEWTuXUAIrlE-?format=jpg&name=large) to do this work quickly. It's true that with React Server Components you may see an increase in overall data transfer in long sessions. But:

1. That data isn't JavaScript that needs to be parsed and executed, and
1. You would have had to do a round trip for the data regardless. Might as well do some of the rendering of that data on the server. 

Also, re: 1., React Server Components render into a "precompiled" instruction to the client that allows React to render the resulting server tree [much quicker](https://twitter.com/dan_abramov/status/1342130504464666625) than it would be if it were done on the client.

> This seems like it'll complicate code bases. I want a clear separation between server and client-rendered components, not an intermingling of the two.

Today we already intermingle data fetching logic in client side JS apps. This often leads to complex state management and data fetching solutions. React Server Components can actually simplify the programming model here. If you had a chance to check out the demo, we had to do very little state management because of this new paradigm. So in many ways I think React Server Components actually help us separate data fetching from interactive client components. 

Architecture wise, I also expect that teams will want to continue to write their backend services in the language of their choice. Frontend teams, if they choose to adopt React Server Components, could create frontend APIs/BFFs (backends for frontends) written in nodejs that compose those backend services. The nice thing here is that you can now do this all in one language and one tech stack. Monolithic architectures however may find this more tricky (ie you'll need to figure out how to run a JS runtime on the server) unless your choice of server language is already JavaScript.

> Server rendering could lead to hard-to-find bugs, especially when it comes to managing user sessions.

I do think this is no different from before. Ultimately, it's going to depend on your team's backend and error reporting infrastructure here.

> This might become *more expensive* for applications. In the search demo, finding those search results plus rendering them on the server is a more expensive operation than just an API call sent from the client.

We are moving some of the rendering to the server–so it's true that your server will be doing more work than before. But server costs are constantly going down, and far more powerful than most consumer devices. I think React Server Components will give you the ability to make that tradeoff and choose where you best want the work to be done, on a _per component_ basis. And that's not something that's easily possible today.

> Streaming HTTP responses (unless they're done with WebSockets, like LiveWire or LiveView) are generally harder and more annoying to implement on your own.

You'll be able to use React Server Components without WebSockets or HTTP/2. In our demo we use chunked encoding which is HTTP/1.1 compatible and straightforward to enable in most server frameworks.

---

### #68 — @davidbarratt — 2020-12-26 15:11

I _think_ this RFC could solve vercel/next.js#11897 and flareact/flareact#93. Sometimes pages can only be rendered on the server, can only be rendered on the client, or can be rendered either way! Right now, projects like Next.js have to make a decision based on where it can be rendered by what methods you have exported on the page component. The only problem I see for that library is: How could they determine when a component needs to be run at runtime, or is safe to run once at build time?

---

### #69 — @josephsavona — 2020-12-26 18:15

> Is this [...] format / server component format going to be react / javascript only?

The exact format for encoding Server Component output (the "Server Component protocol") is currently an internal implementation detail and we expect this format to change -- possibly significantly -- before Server Components are stabilized. We recommend against shipping anything to production that makes assumptions about the exact protocol format for now.

Also note that we actually have two (similar) implementations of this protocol, one that is built on Node.js streams (and used in the demo) and one using plain JSON for embedding inside another JSON-based protocol (and used internally, where in our case we embed the Server Component response inside a GraphQL response). Each of these versions requires support in React, however, so we anticipate having a fairly small number of options provided by React for common situations. 

Support for other programming languages was asked about above, [see my earlier answer](https://github.com/reactjs/rfcs/pull/188#issuecomment-749177032).

> How are breaking changes going to be handled, eg. breaking changes in server component contract?

The short answer is that this is definitely something we are considering as an open area of research (as part of categories such as routing and partial refetching). However this is also something that different frameworks or apps may want to handle differently and we may end up documenting a set of recommendations for frameworks rather than implementing a specific approach as part of React itself.

---

### #70 — @aminpaks — 2020-12-27 15:30

I'm just gonna write this with really good intentions so please don't take it the wrong way.

I've been reading all the negative comments (here, twitter...) and I couldn't say nothing that I really don't understand why people are against the Server Components feature. Please understand that React is an open-source software maintained by Facebook. All React core developers work at Facebook. Most likely Facebook needs this feature for their use-case and the engineers on the team believe implementing the Server Components is the right choice for Facebook's use-case.

**Don't use Server Components if it's not helping your software or use-cases**. Period.

The only time these negative comments would make sense is when React API changes and break your software. It's been 5 years I'm using React and its API has been consistently stable.

Honestly I think some people have a tendency to always see the glass half empty.

---

### #71 — @uasan — 2020-12-28 09:00

I'm surprised why the option, Headless Browser, was not discussed.
For these tasks we successfully use IBM solutions - [Browser Functions](https://github.com/IBM/browser-functions/blob/master/docs/index.md)

This is a truly unified execution environment, understandable and convenient for the entire front-end development team.
The performance and transparency of this approach is much higher than standard SSR solutions.

---

### #72 — @cyphernull — 2020-12-28 09:21

Would React become Rails-like ?

---

### #73 — @rakeshpai — 2020-12-28 13:33

Would be great if usage in service workers would be a consideration. We'd be able to have minimal code in the UI thread, and move most of the bundled code over to a worker / service worker. The "server" code, here running in a service worker, could output strings and a super light-weight UI thread could apply the deltas.

---

### #74 — @Artur93gev — 2020-12-28 14:04

Thanks for good research. Does the size of React itself will be increased, if the application is just using CSR? I mean the serializer of the intermediate representation of the tree is something that will be added to React itself, no matter what environment It will running on?

---

### #75 — @brillout — 2020-12-28 17:26

# [Proposal] Idea to simplify overall design

The restriction that Client Components aren't allowed to import Server Components is the source of complexities. I'm guessing the purpose of this restriction is to avoid the waterfall situation of rendering going back-and-forth between client and server. Is that the main reason for the restriction?

AFAICT removing this restriction would considerably simplify the usage of Server Components, and I'm wondering if removing this restriction is possible, in a performant way:
 - When the server renders a Server Component, all descendants of the Server Component are rendered on the server-side, including all descendant Client Components. (In order to avoid rendering going back-and-forth between client-side and server-side.) Once the virtual dom computing goes server-side it never goes back client-side.
 - Whenever the client-side wants to render a Server Component, the client calls an endpoint `/_react/render` and the server computes and returns the virtual dom and the list of context objects used. The client passes the context objects and the state of all the Server Element's descendant Client Elements so that the server has all the information needed to be able to compute the virtual dom. The client then uses the returned virtual dom to perform reconciliation, and uses the list of used context to know whether to request a re-render whenever a context object changes.
 - When a Client Component is rendered by the server, the server only computes the virtual dom while the hydration on the client-side takes care of running the Client Component's `useEffect` & co. Similarly to what is being done today with SSR where Client Components are allowed to run on the server but hydration takes care of the client-side stuff.
 - The webpack react plugin removes the server component source code from the client-side bundle.

AFAICT this should work, or am I missing something here?

The benefits would be many, amongst others:
 - No routing needed. (Routing can be done simply by having a stateful Client Component orchestrating Server Components.)
 - No central caching `unstable_getCacheForType` and `unstable_useCacheRefresh` needed.
 - The client-side can cache the rendering of Server Components by using `shouldComponentUpdate`/`memo`, preventing unnecessary network round trips.
 - More things can be moved to the server. For example, the note preview (and its included heavy markdown dependency) in the left side panel of the demo can't easily be moved to the server with the current design, but, with the proposed design, this would be trivial.
 - The `/_react/render` is the only Server Components endpoint needed.
 - Migration is easier: add a) the react webpack plugin, and b) the `/_react/render` endpoint &mdash; that's it. Current React 16.x apps work as before and Server Components can be progressively added without changing the app's architecture.

The main and overarching benefit being that I can create components that are concerned only about themselves: no shared infrastructure (no `X-Location`, no `unstable_getCacheForType`, etc.), I can use Server Components wherever I want, and I can write them independently of the rest of the app. When I enter the world of a component I can think locally, whereas the restriction that Client Components aren't allowed to import Server Components forces me to think globally.

Also, this would make it possible to use Server Components without a framework.

What do you think?

I really like Server Components, and if we can simplify its usage it could become quite a perfect thing.

---

### #76 — @jimisaacs — 2020-12-28 17:47

@brillout I don't fully understand your proposal, but I understand and agree with your reasoning for it.

---

### #77 — @resynth1943 — 2020-12-28 19:14

Just saw the proposal on the React website, and watched the demo with the awesome Dan Abramov :-) 
I thought I'd drop by and raise some concerns / proposals for this RFC.

Firstly, I'd like to ask about different versions of React. Let's imagine the server is using React 30 (fake). When the client uses React 31 (fake), which introduces a different protocol schema, what would happen? I bet React would include backwards compatibility for older platforms, as they have done in the past, but this still seems like a valid concern. 

What if server / client components were in separate Git repositories, and the maintainer forgot to update one of them? Has this use-case been covered?

> (To be clear, right now the code is using a, uh, very surprising pattern to make asynchronous code appear synchronous: if the result value is cached, it returns the value synchronously, but if not, the fetcher throws a Promise. You know, you'd normally throw exception objects, but JS lets you throw any value, so why not throw a Promise amirite?!? When React catches a Promise (a thenable) it awaits the result, caches it and then re-runs the React component; now the component won't throw a Promise and will run to completion normally.)

Slightly off-topic, but I've never really liked this pattern. It feels like a hack on language features which were never designed to support this use-case. In most scenarios, `throw` is used to signal fatal errors, not promises to tack on "synchronous" code.

IMHO, this is forcing [algebraic effects](https://overreacted.io/algebraic-effects-for-the-rest-of-us/) into a language which doesn't really support it.

Further to this, I do worry about the **performance implications** of such a mechanism, too. [V8 deoptimises `try` / `catch` blocks](https://bugs.chromium.org/p/v8/issues/detail?id=1065&q=try%20catch&colspec=ID%20Type%20Status%20Priority%20Owner%20Summary%20HW%20OS%20Component%20Stars) and unwinds the stack (IIRC), because it assumes the use of `throw` equates to an application error.

On another note, how much extra code is this functionality going to add to the React package? I've never really been comfortable with React's large bundle size, and I worry **this proposal will append even more bloat for features I'm never going to use.** Could this functionality be replicated with a custom reconciler / renderer?

> Will any part of the server-side be tightly coupled to Node.js, or could it run on a different JS runtime (for example, Rhino in Java, embedded V8 like with ClearScript for C#, ChakraCore, etc)?

I'm shocked to see that nobody has mentioned [Deno](https://deno.land). They support a substantial amount of the major Web API's (WASM, etc.) so I don't see why React wouldn't support this environment. As Deno is up and coming in web development, it's becoming quite a viable platform. Theoretically, if serialisation / deserialisation is decoupled from the HTTP server, support for alternative platforms should carry a low cost.

> Zero-Bundle-Size

This isn't really true though, is it? For starters, you're using a special format which needs to be serialised / deserialised on the client, plus all the extra cruft of communicating with the rendering server.

> Please understand that React is an open-source software maintained by Facebook. All React core developers work at Facebook. Most likely Facebook needs this feature for their use-case and the engineers on the team believe implementing the Server Components is the right choice for Facebook's use-case.

> Don't use Server Components if it's not helping your software or use-cases. Period.

With respect, I think you're missing the point. I've seen some people compare this proposal to Hooks, but I feel like this introduces quite a substantial amount of ambiguity in comparison. There are also concerns about the implications of this proposal on bundle size. Remember, this is a **Request for Comments**, and it should be treated as such. Constructive criticism should be encouraged.

Furthermore, after watching the demo, I'm not sure the end justifies the means with respect to the Notes application. Batching calls to `fetch` can be done without all this extra cruft / server load, so I personally don't believe it gave a solid use-case for this pattern.

P.S. extraneously large dependencies aren't a good demo for this proposal. If you're only using a subset of a large dependency's functionality, perhaps consider swapping it for something else :slightly_smiling_face:

---

### #78 — @aminpaks — 2020-12-28 20:27

>I'm shocked to see that nobody has mentioned Deno. They support a substantial amount of the major Web API's (WASM, etc.) so I don't see why React wouldn't support this environment. As Deno is up and coming in web development, it's becoming quite a viable platform. Theoretically, if serialisation / deserialisation is decoupled from the HTTP server, support for alternative platforms should carry a low cost.

Deno is TypeScript. TypeScript can run JS code without any issue. Designing the server part to be Node.js compatible makes more sense as it covers both.

I'm expecting the server implementation will be designed as an API to plugged into any Node.js servers as a middleware.

> With respect, I think you're missing the point. I've seen some people compare this proposal to Hooks, but I feel like this introduces quite a substantial amount of ambiguity in comparison. There are also concerns about the implications of this proposal on bundle size. Remember, this is a Request for Comments, and it should be treated as such. Constructive criticism should be encouraged.

I wasn't referring to comments like yours. Constructive criticism is always needed and as you mentioned that's exactly why they shared the idea. And with respect again I think you missed my point. I would still let the team implement the feature and if after tree-shaking there was a huge difference in the React core size or breaking backward compatibility then raise the flag. Though I'm sure the React team will design the feature to be modular with stable API as already mentioned.

> Furthermore, after watching the demo, I'm not sure the end justifies the means with respect to the Notes application. Batching calls to fetch can be done without all this extra cruft / server load, so I personally don't believe it gave a solid use-case for this pattern.

Maybe the demo didn't described the use-case well but that demo seems to be a simplified version of their use-case at Facebook and as they mentioned it reduced 29% bundle-size in their app. That should be enough to justify it.

> P.S. extraneously large dependencies aren't a good demo for this proposal. If you're only using a subset of a large dependency's functionality, perhaps consider swapping it for something else

Sometime replacing large dependencies is not an option. So I wouldn't dismiss this fact that easily.

---

### #79 — @resynth1943 — 2020-12-28 22:30

> Deno is TypeScript. TypeScript can run JS code without any issue. Designing the server part to be Node.js compatible makes more sense as it covers both.

I was referring to the use of proprietary Node.js lib modules, which would hamper compatibility with alternative runtimes. While things like accessing the file-system are harder to implement in a cross-platform fashion, I personally believe the serialisation of JSX can be done without any dependencies on Node's standard library.

As I said, it may be worthwhile to decouple the server from the serialisation, so a separate Node-specific middleware function would do nicely.

In theory, if this were implemented as such, React could also be used with web-workers, ~~although I question the usefulness of that pattern.~~ *which seems to be documented as a use-case in the specification.*

> Maybe the demo didn't described the use-case well but that demo seems to be a simplified version of their use-case at Facebook and as they mentioned it reduced 29% bundle-size in their app. That should be enough to justify it.

I'm glad this has gone through real-world testing. That's rather comforting to know. Thanks.

P.S. I left a few review comments, see above :-)

---

### #80 — @aminpaks — 2020-12-28 23:24

> I was referring to the use of proprietary Node.js lib modules, which would hamper compatibility with alternative runtimes. While things like accessing the file-system are harder to implement in a cross-platform fashion, I personally believe the serialisation of JSX can be done without any dependencies on Node's standard library.

That's an interesting point. I'm sure this feature will require some basic FileSystem APIs but that doesn't mean they should live inside React itself and can't be opted-in. A good example of this would be how `React` and `ReactDom` separate the concerns. I would assume the Server Components will have small pieces that work together but they will be framework agnostic. React team has already mentioned this so I wouldn't worry about that for now.

---

### #81 — @yisar — 2020-12-29 03:17

> As I said, it may be worthwhile to decouple the server from the serialisation, so a separate Node-specific middleware function would do nicely.

I totally agree. In fact, there is only one SSR scenario on the server side, and all other scenarios are reverse to back.

But I think this kind of intermediate code is an abstraction, suitable for many places, such as worker-component?

---

### #82 — @drkibitz — 2020-12-29 18:51

Am I missing more detailed info on the JSON format? I can't seem to find anything on it. Was looking for a spec, but it doesn't have to be that far along. Just something that shows and explains an example would be nice. Sorry in advance if I did in fact miss some obvious public place this information exists.

---

### #83 — @ahmetcetin — 2020-12-29 20:42

I don't want to undermine the work done, but server components rather looks like kicking the can down the road to me (can = state management). Instead of getting "data-only" over the wire, now you send "html+css+rendered data". Plus if any child client component uses the data, you send that data as well. Also adding pressure to precious server compute power to render the page is the bonus. 

The benefits of server components:
- cleaner frontend code (less maintenance of state in frontend)
- sending less js code over the wire

When you don't maintain state in frontend, you need to do it in backend. Otherwise you request the same garbage from database server. You save sending garbage data over the wire to browser only, but now you send html+css instead on re-render. Better to use graphql.

"GraphQL doesn't make sense in all cases, for example you write in your small hobby apps...": well, I wouldn't over-engineer my small hobby app for thinking which parts should be rendered on server or client as well.

When I need to optimize my small hobby app, I'm not sure if I'd choose server components over graphql.

About sending less js code: Now you should add a fetch wrapper (react-fetch: 8.4 kb) plus the additional code in react.js to support Server Components.

---

### #84 — @wmertens — 2020-12-30 14:38

@ahmetcetin correction: Server Components aren't just fancy PHP. They don't result in HTML snippets, but in a streaming format that basically seems to serialize `React.createElement` calls combined with Suspense.

I think this is a good idea, and it can certainly improve some harder use cases, like filtering/sorting huge data sets. It is definitely not the best/only way to work. That depends completely on the application.

---

### #85 — @wmertens — 2020-12-30 14:58

What saddens me a bit is that Suspense isn't officially released yet, and now we have this added to the mix. Perhaps because of the interaction with SSR. It looks like SC will be the only way to get Suspense in SSR and thereby streaming single-pass SSR.

But that causes code duplication: if you want to make a Single Page Application that has streaming SSR (for good SEO), you have to use Server Components. But after the app loaded, you want to fetch only the data on the client so you can use a local cache. So then any components that were Server Components and fetching data now need to be Client Components that fetch their own data?

Is there a way to make a Suspense-based data getter work both as a SC and a CC?

```js
const Detail =  id => {
  const item = getItem(id) // uses GraphQL on server and client, throws a Promise while loading
  return <ItemDetail value={item} />
}
```

But it seems to me that a SC is replaced with some sort of proxy in the client vDOM, so once you render once with SC, you're forced to keep rendering on the server, unless you replace the entire vDOM with a duplicate one without SC. This means that you need to write the same logic in `Detail.server.js` and the `Detail.js` that you replace it with.

TL; DR: how to use SC only once on the server and from then on keep using CC?

---

### #86 — @ahmetcetin — 2020-12-30 15:29

@wmertens thanks for the correction, but still if your SC has lots of elements and/or css-in-js, regardless if it's serialized React.createElement or pure html/css, it still needs to send those in rendered component. What bothers me also, btw I didn't test personally, just saw in the demo, if the client child component(s) of the SC are using that data, you send the rendered SC including the data rendered, and additionally sending the raw data to be used by the client, not a good idea. 

My point is, using SC is not a quick and easy solution. You just need to plan well how to organize SC and client components, not only considering the state management, but also styling/interactions, CCs shouldn't require the same data, code duplications etc. 

In some edge cases SC might be useful indeed, but presenting it like a solution to messy state management in frontend, or "I want to write my component that simple", or "using GraphQL doesn't make sense" is not really satisfying.

---

### #87 — @mikestopcontinues — 2020-12-30 15:32

@wmertens You don't need server components for SSR. Regular components (non-server, non-client) will work as they do now regarding SSR. Those components will function as they currently do now. 

You would only add server components to your stack if you need heavy processing or server-specific functionality in your app. In that case, it's still possible to get them to render once for the initial page load (or new route request), by designing them so that they don't need to be re-rendered. This can be accomplished at any level of your app hierarchy by passing server components down your virtual dom tree via props or context. 

I think the important thing to remember given your concern is that regular components aren't going away. Server components don't replace them. Server components handle a very different set of use-cases, allowing you to embed lots of functionality you would have normally outsourced to api endpoints into a single monolithic react app (if you want). 

Perhaps because my project is the ideal use-case for server components, I've found loads of possibilities of how it could help. For instance, right now I have an admin app that embeds a view app in an iframe to show live updates. Using window.postMessage makes all of that functionality more difficult, more slow, and more prone to errors. But with server components, I could merge the two apps, and determine based on authentication if a user should get the very light view-only or the heavier admin-wrapped app. No more postMessage for me, and no extra kbs of logic on the view end to support being embedded in an iframe.

My sales website's blog, help docs, and basic pages are all written in markdown. To keep the site up-to-date without having to redeploy for every change, I have to jump through a ton of hoops. It requires piles of mental overhead. And for a single developer actively developing over 2M lines of code, it would be much nicer to collapse that complexity down. No more api endpoints. Just a server component that hits the github api, converts the markdown to html, and caches the result for that particular set of props. Right now, it's a Next route that hits an api that does the processing, then passes that data down to a component that does the rendering. One file vs three at minimum, more in practice.

---

### #88 — @wmertens — 2020-12-30 16:24

@mikestopcontinues Yes, SSR works right now for me, but I have to run 2 render passes (the first one to trigger data fetches) and I can't stream. I would like to use Suspense so that I can do the SSR using a single pass. It looks like Suspense in SSR will only be available via SC.

Passing the SC down the tree is interesting, so you import the component and then pass it as a prop, to get around the importing server code rule in CC, right? So that might be used to, in the browser, replace a SC with an equivalent CC that uses graphql. Hmmm. Too bad there's no such thing as a "server hook", I like using hooks for GraphQL and polymorphic SC/CC would require using components again, ah well.

You give good examples, I totally agree SC is very useful for resource heavy things and I'll be happy to have it in the toolbox.

@ahmetcetin no, the SC will basically generate the props that are needed for rendering, and then send that to the client. The client will load the CC it needs to render, give them the props and they will render. CSS-in-JS will be entirely in CC, it can't work on server-side. So if you have complex DOMs, it's best to use SC only to generate props and pass it to client components. I think.

---

### #89 — @lucasecdb — 2020-12-30 17:13

> Passing the SC down the tree is interesting, so you import the component and then pass it as a prop, to get around the importing server code rule in CC, right?

@wmertens you wouldn't be able to do that because the component can't be serialized to pass it from a SC to CC.

---

### #90 — @wmertens — 2020-12-30 17:44

@lucasecdb that was what I thought at first, probably a CC is a boundary for rendering? Then it won't be able to call the SC indeed.

Universal components would work but they would mean a lot of duplication in the SC render response if you have to do prop passing

---

### #91 — @lucasecdb — 2020-12-30 17:58

> @lucasecdb that was what I thought at first, probably a CC is a boundary for rendering? Then it won't be able to call the SC indeed.

yeah, when React is rendering the server component tree it replaces the client imports with a ["client reference"](https://github.com/reactjs/rfcs/blob/235f27c12aa893efd2378ec3c4a9b0b221641861/text/0000-server-module-conventions.md#implicit-client-references), which it will use during the reconciling process to determine which client components needs to be rendered. This way you can't even use the client component implementation because the webpack plugin is literally replacing it with a static reference. Even if you tried to call the CC function you couldn't (you can try this and see the error in the demo).

---

### #92 — @gaithoben — 2020-12-30 18:21

Server components streaming back HTML would solve all my problems with SSR. Otherwise, the project is, to say the least very interesting to follow.

---

### #93 — @josephsavona — 2020-12-30 19:20

@brillout Thanks for moving your proposal back into the main RFC, it helps us keep discussion focused!

> The restriction that Client Components aren't allowed to import Server Components is the source of complexities. I'm guessing the purpose of this restriction is to avoid the waterfall situation of rendering going back-and-forth between client and server. Is that the main reason for the restriction?

Not quite: the reason is that Server Components allow direct access to server-only resources such as filesystems, databases, etc. So they can't be imported by Client Components because *they can't run on the client*. But it *is* possible to fetch the results of Server Components from Client Components: that's what the Notes demo app is doing to load basically the entire page - note that there's actually one client component at the root. This means that you could, if you chose, fetch multiple distinct Server Components at different levels of your app to create waterfalls and hurt your app's performance. It isn't prevented by this proposal.

However, we are intentionally not encouraging that as a pattern because *it's already easy to introduce waterfalls in React apps*. These waterfalls are a common source of performance problems, and the idea of Server Components is to give developers an easy to use, powerful approach for *avoiding* client/server waterfalls. 

> [...] this would make it possible to use Server Components without a framework. What do you think?

First, note that *you won't have to use a framework to use Server Components*. We are *starting* with some framework integrations in order to make it easy to try using Server Components and to provide an example of how you can integrate them into your app, but you won't be required to use a framework. 

As for the proposal, I'm skipping over quoting the details for brevity, but my interpretation of your idea boils to two key pieces:
* Allowing importing SC from CC, but swap them out so that rendering the SC causes its output to be fetched
* Have a mechanism that exposes an endpoint for the SC output to be fetched.

This is roughly analogous to the key integration pieces proposed by this proposal already: a special mechanism for importing CC from SC, and framework/app integrations for matching routes to SC. So it doesn't appear that this proposal ultimately simplifies the implementation or that it provides new capabilities not already achievable (as noted above, you can already go out of your way to create waterfalls if you want to). 

> I really like Server Components, and if we can simplify its usage it could become quite a perfect thing.

We agree! I definitely encourage trying out Server Components to get a feel for developing with them. As we started building our first apps with SC we had a lot of "aha" moments when we realized that Server Components let us achieve things we hadn't even considered initially. That said, yes we absolutely will consider ways to improve Server Components based on user feedback.

---

### #94 — @josephsavona — 2020-12-30 19:33

> Firstly, I'd like to ask about different versions of React. Let's imagine the server is using React 30 (fake). When the client uses React 31 (fake), which introduces a different protocol schema, what would happen? I bet React would include backwards compatibility for older platforms, as they have done in the past, but this still seems like a valid concern.

@resynth1943 Versioning is something we're still evaluating. We haven't decided on an approach here but it's very much on our radar.

> IMHO, this is forcing algebraic effects into a language which doesn't really support it.

A similar concern was raised above re the Suspense mechanism and why not use an alternative such as async/await (see the [FAQ](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#why-not-use-asyncawait)). We plan to write a separate RFC to document the design of Suspense and the various tradeoffs that led us to the current approach.

---

### #95 — @josephsavona — 2020-12-30 19:36

> Am I missing more detailed info on the JSON format? I can't seem to find anything on it. Was looking for a spec, but it doesn't have to be that far along. Just something that shows and explains an example would be nice. Sorry in advance if I did in fact miss some obvious public place this information exists.

@drkibitz No, you're not missing something! We haven't published details of the response format yet as it's an internal implementation detail that is highly likely to change.

---

### #96 — @wmertens — 2020-12-30 19:39

@josephsavona what are your thoughts on using SC on the server once for enabling single-pass streaming SSR, and then somehow only using CC+regular components on the client, never rendering those SC again? https://github.com/reactjs/rfcs/pull/188#issuecomment-752651155

---

### #97 — @josephsavona — 2020-12-30 19:39

(aside: I replied to a few questions/ideas that stood out and appeared not to have already been answered by other commenters. I'm out of time but I or other team members will check in on the discussion after the new year).

@wmertens sorry just saw that last one, will answer when i have some more time!

---

### #98 — @MohitPopli — 2020-12-31 06:26

IMO decreasing bundle size will help people a lot but at the same time some people will argue of introducing such complexity into react applications. But I think it's too early to decide on this.

I want to know that with this Server components concept Server Sent Events mechanism will work as expected or will there be any change in that too? 

Seeing video makes this pretty clear that we cannot have any sought of animation/ client interaction with components rendering on server side. I am curious to know why it is a challenge to support that?

---

### #99 — @drkibitz — 2020-12-31 08:16

The utility of server components lies on the flexibility of the wire format. The reason for this is because I believe a client, can and should be able to benefit without requiring any corresponding server infrastructure and maintenance. Take PHP, the reason it exploded years ago wasn't because of the syntax, but because of how easy it was for hosting providers to offer it in a shared and very affordable environment, and by affordability, I am not only talking about money. I believe whatever the format may become, it should aim to be the foundation to stand a possible shared server component environment. Where is this coming from? It is rather easy to imagine that an initial version of all this (maybe this version) couples the client with the server so much, that the format is actually dependent on component definitions mutually understood by the server and client. To keep the format as compact as possible increases the likelihood of this coupling. Without going into too much detail, or writing a full proposal here, I would just want to suggest one thing. That is that the format is based on decoupled component definitions, with importable / exportable schemas. I would like to imagine a client that may be built with a server component schema, to communicate and depend on that server's components, regardless of whether that particular client is actually served by that particular server.

---

### #100 — @wmertens — 2020-12-31 08:39

@drkibitz no worries, the coupling happens via bundler ids. As long as all servers are running and serving the same code, any server can handle a render request for SC

---

### #101 — @gaearon — 2021-01-02 17:18

>Security: for each http request (even if the domain is localhost) the server components will be performing, what if there is an access token needed? What if there is an authentication and authorisation needed, should the server components authenticate themselves first, and ask for an access token to be authorised to access some data resources?

>Maintenance costs : if the server that is responsible for the rendering of our server components is no longer reachable for some reason (say DDOS attack), does this mean that we will have to handle a new type of errors, errors of type: component currently not available? And could this be properly tested ?

Server Components shift some rendering work to the server, but in many aspects you can think of their refetches as you would about any API calls. I don't know what would make these points different compared to how you normally deploy and interact with an API.

>Performance: could we cache the server render result of a given server component when the input is the same?

Theoretically, yes. In practice, we won't be focusing on this in the initial iteration, but might explore this in the future. React I/O libraries would need to be aware of this caching mechanism.

>Are optimistic updates/rollbacks something that this proposals plans to tackle on or leave to userland solutions?

For many user interfaces, we've come to a conclusion that naïve optimistic updates are _not_ the right user experience. E.g. if posting a piece of content makes it immediately appear in the list, the user might close the tab before the mutation goes through. So we're thinking that in well-designed UIs, many optimistic updates should actually have a separate design (e.g. a "posting" shim with a progress bar) instead of just putting things into the cache. Such a shim would be a Client Component, so it fits into the paradigm despite the real refetch happening through the Server. This also solves the problem that server output might end up being different (e.g. due to post-processing). Of course, you can keep specific interactions (e.g. "liking" a post) fully Client-side.

>One last thing I'd like to see more discussion on is how data fetched on the server can be automatically passed to the client to use as the initial value for a cache, without needing to manually extract it on each request and pass it as a prop.

Can you be more specific? Are we talking about SSR, or about Server Components (or how they work together)? The neat thing about Server Components is that you don't really need to serialize _the cache itself_ because it's really the render output that you're after. The cache that runs on the client only caches _server responses_, but the data you've fetched on the server isn't even needed by the client. Only the rendered result.

>Many data fetching libraries populate some kind of external cache so that you can read from that in many parts of an application without having to pass props down. It is likely that both server and client components will want to use the same data, so those solutions will still be important in many apps.

With the idiomatic Server Components model, you "pass" things by passing props to Client Components. Including refetches. Nothing more, nothing less. This is a different model than traditional normalized caches — it's denormalized. In this model, the client doesn't _need_ the normalized data because you prepare the render result on the server.

It's hard for me to comment in more detail unless you expand on this point with a more specific scenario. But broadly speaking, Server Components don't require transferring the server cache to the client.

>The performance and transparency of this approach is much higher than standard SSR solutions.

I find it very challenging to believe that a Node server talking to the browser can be more performant and less resource-intensive than a Node server alone.

>Would React become Rails-like ?

No, but it should provide better building blocks if you want to build something Rails-like on top.

>Would be great if usage in service workers would be a consideration. We'd be able to have minimal code in the UI thread, and move most of the bundled code over to a worker / service worker. The "server" code, here running in a service worker, could output strings and a super light-weight UI thread could apply the deltas.

This is actually what we *started* with in 2014. This experiment didn't pan out for various reasons (https://github.com/facebook/react/issues/7942#issuecomment-254984862) and gave us insights for the current React architecture and its approach to concurrency. But the idea of two types of components originally comes from that research.

>Does the size of React itself will be increased, if the application is just using CSR? I mean the serializer of the intermediate representation of the tree is something that will be added to React itself, no matter what environment It will running on?

>On another note, how much extra code is this functionality going to add to the React package? I've never really been comfortable with React's large bundle size, and I worry this proposal will append even more bloat for features I'm never going to use. Could this functionality be replicated with a custom reconciler / renderer?

There are some things we're adding to the Client-side React, but they're useful on Client-only too. Such as just general support for Suspense data fetching. These features are currently within range of 1% to 3% as far as I know.

The (de)serializer is separate and won't get pulled in if you're not using it. So you're not paying the cost for what you don't use.

>Firstly, I'd like to ask about different versions of React. Let's imagine the server is using React 30 (fake). When the client uses React 31 (fake), which introduces a different protocol schema, what would happen? I bet React would include backwards compatibility for older platforms, as they have done in the past, but this still seems like a valid concern.

The intended integration would be through frameworks (or your own infra that works the same way). A framework would always use one version of React. There are questions about what happens during deployment, but it's a more general question (and not just about upgrading React) and the solutions there are also more general.

>What if server / client components were in separate Git repositories, and the maintainer forgot to update one of them? Has this use-case been covered?

I don't understand how this is different from what you get today in a server-rendered app.

>Slightly off-topic, but I've never really liked this pattern. It feels like a hack on language features which were never designed to support this use-case. In most scenarios, throw is used to signal fatal errors, not promises to tack on "synchronous" code.

Thanks, we're definitely aware of what `throw` is used for. As noted several times throughout this thread, we will write another RFC to explain why we think this is the right approach given all the tradeoffs. I'd like to ask to not focus on this in this thread because there'll be another one.

>I'm shocked to see that nobody has mentioned Deno. They support a substantial amount of the major Web API's (WASM, etc.) so I don't see why React wouldn't support this environment. As Deno is up and coming in web development, it's becoming quite a viable platform. Theoretically, if serialisation / deserialisation is decoupled from the HTTP server, support for alternative platforms should carry a low cost.

Sure, we'd be happy to accept a PR for Deno bindings. As you correctly say, as long as something can run JavaScript code and has some kind of streaming API, we can very likely make it work.

>This isn't really true though, is it? For starters, you're using a special format which needs to be serialised / deserialised on the client, plus all the extra cruft of communicating with the rendering server.

The point is that you can keep adding zero-cost abstraction layers on the Server while being confident that your bundle size doesn't keep growing one bit. I don't see how this isn't true.

>P.S. extraneously large dependencies aren't a good demo for this proposal. If you're only using a subset of a large dependency's functionality, perhaps consider swapping it for something else 🙂

Judging by the community response, heavy dependencies _are_ very much a pain point. Yes, any small demo is going to feel convoluted, but having the freedom to add arbitrary dependencies without the bundle size cost is something people clearly appreciate so far.

>I was referring to the use of proprietary Node.js lib modules, which would hamper compatibility with alternative runtimes.

You can make your own React I/O bindings to any modules. In fact part of the idea behind `react-fetch`, `react-fs` and others, is that constrained cloud environments could even swap them out for more "native" implementations where it makes sense.

>Am I missing more detailed info on the JSON format? I can't seem to find anything on it. Was looking for a spec, but it doesn't have to be that far along. Just something that shows and explains an example would be nice. Sorry in advance if I did in fact miss some obvious public place this information exists.

It's an implementation detail that's expected to change a lot over time. There is [some grammar description here](https://github.com/facebook/react/blob/50393dc3a0c59cfefd349d31992256efd6f8c261/packages/react-server/src/ReactFlightServerConfigStream.js#L14-L62).

>When I need to optimize my small hobby app, I'm not sure if I'd choose server components over graphql.

You're welcome to keep using GraphQL if it works well for you.

>Perhaps because of the interaction with SSR. It looks like SC will be the only way to get Suspense in SSR and thereby streaming single-pass SSR.

Yes, this is the current plan.

>But that causes code duplication: if you want to make a Single Page Application that has streaming SSR (for good SEO), you have to use Server Components. But after the app loaded, you want to fetch only the data on the client so you can use a local cache. So then any components that were Server Components and fetching data now need to be Client Components that fetch their own data?

I don't follow this argument. Using SSR doesn't really affect the refetching strategy. When you want to refetch, you send a request to the Server, and it delivers the updated Server tree in the response. That's what's being rendered (and cached) on the client. Like in the demo.

>This means that you need to write the same logic in Detail.server.js and the Detail.js that you replace it with.

Sorry, I don't follow this at all.

>TL; DR: how to use SC only once on the server and from then on keep using CC?

No, but I don't understand why you'd want that.

>What bothers me also, btw I didn't test personally, just saw in the demo, if the client child component(s) of the SC are using that data, you send the rendered SC including the data rendered, and additionally sending the raw data to be used by the client, not a good idea.

>My point is, using SC is not a quick and easy solution. You just need to plan well how to organize SC and client components, not only considering the state management, but also styling/interactions, CCs shouldn't require the same data, code duplications etc.

We already use "references" in the protocol for the same objects so they never appear twice in the output stream. We could conceivably do something similar for strings if that proves to be a problem. We haven't seen that be a problem in our production testing yet. I think you're worrying about a premature optimization here. Also, we shouldn't lose sight of how much data and code we're _not_ sending because it's not needed by the client anymore.

As for styling, it's definitely an open research area but it's not something you would need to worry about _as a developer_. It's something we need to figure out.

---

### #102 — @gaearon — 2021-01-02 17:33

> To keep the format as compact as possible increases the likelihood of this coupling. Without going into too much detail, or writing a full proposal here, I would just want to suggest one thing. That is that the format is based on decoupled component definitions, with importable / exportable schemas. I would like to imagine a client that may be built with a server component schema, to communicate and depend on that server's components, regardless of whether that particular client is actually served by that particular server.

I struggle to follow this comment. I think you're imagining the format as something much more complicated than it really is. It's just a stream where every row is either a JSON object with "placeholders" or some instructions ("load a module"). This format is an implementation detail and no one is expected to care about it or interact with it directly. It's essentially a serialized React tree.

>Seeing video makes this pretty clear that we cannot have any sought of animation/ client interaction with components rendering on server side. I am curious to know why it is a challenge to support that?

I'm not sure what you mean by this. The video actually does show a moment where we can animate something _based_ on a server response. That's a novel part compared to the traditional server rendering. But yes, interactivity is achieved by Client Components. I don't know why you'd want that to be different. Maybe you can expand?

---

Re: https://github.com/reactjs/rfcs/pull/188#issuecomment-751797544

>The restriction that Client Components aren't allowed to import Server Components is the source of complexities. I'm guessing the purpose of this restriction is to avoid the waterfall situation of rendering going back-and-forth between client and server. Is that the main reason for the restriction?

Yes. I'm not sure I would call that a "source of complexities" though because you could argue that _allowing_ that would be a "source of complexities" (just different ones).

>AFAICT this should work, or am I missing something here?

Passing the state of all Client components back to the server makes this a non-starter because (a) much of the state is not, and cannot, be serializable, (b) latency for interactions like inputs makes it impractical, (c) it would spend too much bandwidth. This is what was bad about approaches like ASP .NET WebForms, which is exactly what we're trying to avoid with this design.

Maybe I'm missing something important about your proposal but I don't see how it could work.

---

### #103 — @wmertens — 2021-01-02 20:15

Suppose you want to use SC for a table view somewhere deep in the app, would this eventually be possible or does that mean using an iframe?

---

### #104 — @wmertens — 2021-01-02 20:20

> > TL; DR: how to use SC only once on the server and from then on keep using CC?

> No, but I don't understand why you'd want that.

Client side caching allows quick switching between views without relying on the server, as well as using the same data in different components. When using SC, you can't easily cache the initial nor subsequent render data on the client.

---

### #105 — @brillout — 2021-01-02 21:31

@gaearon

> (b) latency for interactions like inputs makes it impractical

There is no latency for interactions since CCs still mostly re-render on client-side only. Only when an ancestor SC re-renders does a CC render on the server-side.

For example:

~~~jsx
<App> {/* SC */}
  <Header/> {/* SC */}
  <LeftSideBar />  {/* CC */}
  <MainView> {/* SC */}
    <MyForm> {/* CC */}
      <input type="text"/> {/* CC */}
    </MyForm>
  </MainView>
  <Footer/> {/* SC */}
</App>
~~~

Where `<MyForm>`, `<input>`, and `<LeftSideBar>` are CCs while the other components are SCs.

In this example, the SCs are never re-rendered and the state of `<MyForm />` and `<input />` is never sent to the server. (If the state of the CC `<LeftSideBar />` changes, only its children re-render and no SC re-renders.)

Are there situations where a form state would be sent to the server? Yes and AFAICT these situations make sense. For example:

```jsx
<App>
  <Header/>
  <LeftSideBar />
  <MainView>
    {/* `<TabSelection />` is a CC. The user can choose between
        three tabs: `all notes`, `my favorite notes`, `new note`
    */}
    <TabSelection>{selectedTab => {
      if( selectedTab === 'all-notes' ){
        return <AllNotes />;
      }
      if( selectedTab === 'favorite-notes' ){
        return <FavoriteNotes />;
      }
      if( selectedTab === 'new-note' ){
        return (
          <NoteCreator> {/* SC */}
            <SomeStaticTextExplaingStuff /> {/* SC */}
            <NoteForm> {/* CC */}
              <input type="text"/> {/* CC */}
            </NoteForm>
          </NoteCreator>
        );
      }
    }}</TabSelection>
  </MainView>
  <Footer/>
</App>
```

In this example, the state of the form is only sent to the server when the user switches tabs. When the user merely inputs some text in the form, no SC is re-rendered and no CC state is sent to the server.

In general, forms are highly interactive and I wouldn't know why an app developer would want to try to server-side render forms.

> (a) much of the state is not, and cannot, be serializable

Yes, when state is not serializable React would have to throw. But, the way I see it, that's still better than never sending state to the server and therefore completely forbidding CCs from importing SCs.

Any information passed from the client to the server needs to be serializable anyways and, from a serialization point of view, it doesn't make a difference whether the information is saved as a state of a CC or saved in something like `X-Location`.

> (c) it would spend too much bandwidth

Only the state of CC elements, that are descending the SC element being re-rendered, are passed to the server.

This means that if the app never imports a SC from a CC, then CC state will never be sent to the server.

My proposal removes the restriction that CCs are forbidden to import SCs, but users can still choose to never import SCs from CCs. In that case my propsal makes no difference at all.

Waterfalls are avoided with:
> - When the server renders a Server Component, all descendants of the Server Component are rendered on the server-side, including all descendant Client Components. (In order to avoid rendering going back-and-forth between client-side and server-side.) Once the virtual dom computing goes server-side it never goes back client-side.

---

### #106 — @brillout — 2021-01-02 21:59

@josephsavona

> This means that you could, if you chose, fetch multiple distinct Server Components at different levels of your app

My proposal is precisely about enabling this in a performant and user-friendly way.

> waterfalls and hurt your app's performance.

My proposal does address the waterfall problem:

> - When the server renders a Server Component, all descendants of the Server Component are rendered on the server-side, including all descendant Client Components. (In order to avoid rendering going back-and-forth between client-side and server-side.) Once the virtual dom computing goes server-side it never goes back client-side.

What I mean with `In order to avoid rendering going back-and-forth between client-side and server-side` is what you call waterfalls.

> So it doesn't appear that this proposal ultimately simplifies the implementation or that it provides new capabilities not already achievable

Let me clarify with an example why the restriction that CCs aren't allowed to import SCs is a fundamental problem.


### Example, showcasing the fundamental problem of the CC->SC restriction

Let's imagine a spotify-like mobile app with 3 tabs: "Playing Song | Artist Info | Related Songs".

Usually with React, this is implemented with a stateful Client Component which tracks what tab is currently selected. For example, a `<TabSelection />` component with a state `selectedTab`:

```js
<App>
  <MainView>
    <TabSelection>{selectedTab => {
      if( selectedTab === 'playing-song' ){
        return <PlayingSong />;
      }
      if( selectedTab === 'artist-info' ){
        return <ArtistInfo />;
      }
      if( selectedTab === 'related-songs' ){
        return <RelatedSongs />;
      }
    }}</TabSelection>
  </MainView>
  <SideBar />
</App>
```

The `<ArtistInfo />` component would be non-interactive and we want `<ArtistInfo />` to be rendered only server-side.

The server doesn't know the state `selectedTab` and, because of the CC->SC import restriction, there is no intuitive way of passing `selectedTab` to the server. This means that the server cannot know whether to render `<PlayingSong />`, `<ArtistInfo />`, or `<RelatedSongs />`, and ultimately `<ArtistInfo />` cannot be rendered by the server.

One way to solve this is to move the `selectedTab` state further up the tree in a server-side central piece of architecture, which is basically what `X-Location` and the whole caching thing of the notes demo is about. This breaks encapsulation/colocation: I cannot think about `<MainView>` in isolation and some logic of `<MainView />` is now living in a central piece of architecture. Also, it's not very idiomatic React code.

Bottom line: the CC->SC import restriction forces us to move all state, that the server needs to know about, up in the tree, before any CC.

In contrast, with my proposal, it would be possible to keep the stateful CC `TabSelection` and its `selectedTab` state, while `<ArtistInfo>` is a SC: the CC `<TabSelection>` would simply import and use the SC `<ArtistInfo>`. The neat thing here: it's idiomatic React code and there is no need for any central routing/caching mechanism.

In this example, moving the information which tab is selected to a central mechanism would be a okay-ish solution. But you can imagine other examples where this becomes a mess. For example, imagine the Facebook main page: it has a news feed, several chat windows, a list of online friends, etc. It would become quite messy if all states that the server needs to know about end up in one central place.


### Proposal Summary

My proposal can be summed up in three parts:
1. Allow CCs to be run and rendered by the server. (While the client-side performs hydration, similarly to SSR.)
2. Allow CCs to import SCs. (Using the webpack plugin to replace the source code of SCs with code that requests & fetchs the server-side rendering of the SC.)
3. While rendering the app tree, when a branch goes server-side, it never goes back client-side. (To avoid waterfalls.)

I don't know if my proposal has a structural flaw I'm not seeing, but I'm seeing the SC->SC restriction to be the main problem about the current design and if we can get rid of it that'd be lovely.

---

### #107 — @gaearon — 2021-01-02 23:37

@wmertens

>Suppose you want to use SC for a table view somewhere deep in the app, would this eventually be possible or does that mean using an iframe?

This is a bit vague (what does "deep" mean? probably not the number of layers but some other aspect?) but yes, I don't see why this wouldn't be possible. It's a Server tree refetch that instructs to load and render that particular subtree (which itself includes the table). How this works exactly is still part of the ongoing research and won't move further until we at least implement Server Context (which would let us refetch Server subtrees without always rendering from the root). So while the details are out of scope of this discussion, this use case is definitely something we need to support.

>When using SC, you can't easily cache the initial nor subsequent render data on the client.

This doesn't sound right. If you look at the demo, when you switch between Notes that have already been fetched, there is no refetching. There is client caching happening — *of the Server responses themselves*. You don't need to move fetching to Client Components to benefit from caching. Rather, caching is a layer provided by React that both Server and Client components (and Server responses on the client) can benefit from. Again, the exact semantics and APIs are out of scope of this discussion, but caching is a very important part of the model.

---

### #108 — @gaearon — 2021-01-02 23:47

>Yes, when state is not serializable React would have to throw. But, the way I see it, that's still better than never sending state to the server and therefore completely forbidding CCs from importing SCs.

I think this still makes the idea a non-starter. State cannot be expected to be serializable, it can be incredibly heavy to transport (e.g. holding thousands of rows in state is pretty normal). It also makes writing Client components a minefield because you can never trust that someone doesn't already use this component inside a Server tree. In which case adding any non-serializable state would be a breaking change for the Client Component author in this paradigm. In practice it means that nobody would be able to use Server Components because they'd constrain any Client Component inside the tree too much.

---

### #109 — @gaearon — 2021-01-02 23:51

>One way to solve this is to move the selectedTab state further up the tree in a server-side central piece of architecture, which is basically what X-Location and the whole caching thing of the notes demo is about. This breaks encapsulation/colocation: I cannot think about <MainView> in isolation and some logic of <MainView /> is now living in a central piece of architecture. Also, it's not very idiomatic React code.

Right. This isn't quite idiomatic because we're missing support for Server Context. This would be a thing that *does* "survive" refetches by being serializable from the server to the client _and back_. It would have to be extremely slim for that reason, and should probably primarily be used by the routing integration. In that world, `selectedTab` is a part of the route (even if that conceptual "route" isn't actually represented by the URL — although in many cases it probably should be!)

The routing infrastructure would live at the top of the tree, but the actual Server Context would be passed to it from the bottom — so it would be opaque to the router. We would not have the problem where the top level has to have global knowledge.

In other words, the whole cache/location thing is meant to be potentially recursive instead of hoisted at the top level. There are missing primitives in React that prevent us from exploring the actual design at the moment, but it's a very important follow-up.

---

### #110 — @gaearon — 2021-01-03 00:04

So @wmertens brought up frames earlier, and while we wouldn't *use* frames, you might find them a useful mental model for how we imagine the routing system in broad strokes.

You can imagine that each "content area" (like a tab bar) is really a container of "frames". Only one frame is visible at the moment (the selected one). When you switch the tab, the `<TabSelection>` from your example is a Client Component that only toggles the visibility of the frames below it, showing the selected one. If the frame doesn't have content in it, it gets fetched (otherwise, we show the cached content). The frame doesn't fetch the entire Server tree — only the subset from the frame's "position" in the tree. It "knows" all Server Context above it from when it was rendered, so it passes it back to the Server, which is what lets the Server render "from that place below". Child content areas get their initial "frame" preloaded that way from the server. In fact, you can think of tab links themselves as storage for the "preloaded" content that could be in part optimistically streamed at a lower priority — making navigations instant for the tabs we expect to need with high probability.

Like React itself, this design would be recursive and composable, which I think should address your concern.

Again, **we're not actually going to use frames**, this is just an exercise for imagination. There is a lot to work out here and I'd prefer that we don't dive too much into this question yet because we don't actually have many answers yet. But I assure you that compositionality is top of mind for us, and we wouldn't be satisfied by hoisting tree-below concerns up in the tree either.

---

### #111 — @gaearon — 2021-01-03 00:19

I should probably note (to address @wmertens use case more directly) that of course it *is* technically possible to render a Server tree at arbitrary points inside the Client tree. If that wasn't possible, our demo wouldn't work, since our demo is a Client application talking to the Server. It needs to "start" talking to the Server somewhere. That happens in the Client tree.

(This is different from the technical limitation on imports. You can't _import_ a Server component from a Client one, but you can definitely render the infrastructure that does the actual Server API call — in our demo, `Root.client.js` does it.)

So technically nothing would stop you from rendering the Server "table" somewhere arbitrarily deep. *However*, because this would introduce a waterfall if you land directly on this screen (e.g. due to a route), we're hoping to have an idiomatic solution for deep routing which would let you do what you describe _without_ a waterfall. So that you're not _encouraged_ to create more "entry points" into the Server, and instead use the one provided by your routing solution.

In general, I'm not quite seeing how this use case is different from the fact that `<Note>` fetches its own data in our demo. You could wrap it in many Client layers, but you can still compose the Server parts inside. The real missing part now is the ability to cache/refetch _that part alone_, without refetching the whole app. That's the follow-up work.

---

### #112 — @brillout — 2021-01-03 07:53

> it can be incredibly heavy to transport (e.g. holding thousands of rows in state is pretty normal)

Ok I see, that's a problem. (I was thinking more about states that save user actions, which are pretty much always slim. I didn't think about state that holds network fetched data, which can be heavy.)

I'll think about this.

One thing I was thinking is to forbid users to render stateful CCs on the server-side. Maybe this could solve the problem while staying user-friendly. I'll think about this.

>  Server Context

Neat.

---

### #113 — @brillout — 2021-01-03 11:15

I just realized that your other comments are also about my proposal. Interesting ideas. I'll think about them and see how Server Contexts can adress all my concerns.

Spontaneously, I still feel like my proposal to be a simpler solution. (AFAICT, forbidding stateful CCs to re-render on the server would be a solution to the heavy/unserializable state problem; the benefits of my propsal are still there, albeit slighlty less simple than I originally thought.) But I'm going to think through your Server Context solution. I'm also just thinking that maybe something like Server CC State (obviously saved by the client; the server-side should remain stateless) could maybe be a thing, I don't know.

>  I assure you that compositionality is top of mind for us, and we wouldn't be satisfied by hoisting tree-below concerns up in the tree either.

Cool

---

### #114 — @gaearon — 2021-01-03 16:08

> forbidding stateful CCs to re-render on the server would be a solution to the heavy/unserializable state problem

If we were to forbid that, then you effectively couldn’t nest Client components into the Server trees at all, which largely defeats the purpose of the proposal.

---

### #115 — @brillout — 2021-01-03 16:52

> If we were to forbid that, then you effectively couldn’t nest Client components into the Server trees at all, which largely defeats the purpose of the proposal.

You could still have one layer of CCs between an upper and lower layer of SCs. (The upper SC layer is always static and never induces a re-render.)

```jsx
<App>
  <Header/>             {/* Upper SC layer */}
  <Content>
    <TabSelection>{selectedTab => {    {/* Middle CC layer */}
      if( selectedTab === 'all-notes' ){
        return <AllNotes />; {/* Lower SC level */}
      }
      if( selectedTab === 'favorite-notes' ){
        return <FavoriteNotes />; {/* Lower SC level */}
      }
      if( selectedTab === 'new-note' ){
        return (
          <NoteCreator> {/* CC */}
            <SomeStaticTextExplaingStuff /> {/* CC */}
            <form> {/* CC */}
              <input type="text"/> {/* CC */}
            </form>
          </NoteCreator>
        );
      }
    }}</TabSelection>
  </Content>
  <Footer/>
</App>
```

When the tab is selected to `new-note` there is no lower SC layer, because the `<input>` is a CC and forces everything between itself and the CC `<TabSelection>` to be a CC.

This sandwich approach has the advantage that "conceptual routing" can be managed simply by having a stateful CC.

But yes, this sandwich approach does defeat the one purpose I had of "full & easy intermingling of CCs and SCs".

---

### #116 — @brillout — 2021-01-03 21:52

> You can imagine that each "content area" (like a tab bar) is really a container of "frames" [...]

This is how I interpret how it would work:

```js
// Content.server.jsx

// `<TabSelection>` is a CC
import TabSelection from './TabSelection.client';
import { useServerContext } from React;

// `<Content>` is a SC
function Content({preload}) {
   // The client knows that `<Content>` has a dependency on the Server Context `selectedTab`; whenever
   // the Server Context `selectedTab` changes, the client requests & fetches a re-render of <Content />
   const selectedTab = useServerContext('selectedTab');

   return (
     <TabSelection
       tab1={<AllNotes preload={preload} isSelected={selectedTab==='tab1'}/>}
       tab2={<FavoritesNotes preload={preload} isSelected={selectedTab==='tab2'}/>}
     />
   );
}

// `<AllNotes>` is a SC
fuction AllNotes({preload, isSelected}) {
   if( !preload && !isSelected){
     return null;
   }

   return (
     <div renderPriority={isSelected ? 'high' : 'low'}>
       {/*...*/}
     </div>
   );
}

// `<FavoritesNotes>` is a SC
function FavoritesNotes({preload, isSelected}) {
   // Similar thing
}
```

When the user clicks on another tab, the CC `<TabSelection>` changes the Server Context `selectedTab` (which is used to pass information to the server, and to trigger a re-render as explained in the code snippet) as well as a CC state `showTab` (which toggles wich tab is shown to the user).

Is this broadly how it would work?

If I'm foreseeing the whole thing correctly, it would tend to turn CCs into "dumb" stateful components; logic would mostly be implemented by SCs, while CCs would be used to react to user actions and change Server Contexts accordingly, and client-side CC state is mostly used for interactivity.

I'm glad that you care about getting rid of this central routing/caching thing (or I should more precisely say that you want to hide it from app developers).

> we're hoping to have an idiomatic solution for deep routing which would let you do what you describe without a waterfall.

AFAICT, my sandwich solution would solve this. Let me know if it's not clear why and I'll elaborate.

---

### #117 — @brillout — 2021-01-04 07:55

> State cannot be expected to be serializable

> It also makes writing Client components a minefield because you can never trust that someone doesn't already use this component inside a Server tree

The CC author could mark CC state to be serializable and sendable to the server: `useState(initialState, {sendableToServer: true})`.

Without `sendableToServer` the CC can only be used within a SC sandwich layer, and with `sendableToServer` the CC author can enable its CC to be used at any level.

With Server Components, data would tend to be fetched by "suspensed" SCs instead of stateful CCs, and I could see much(/most?) CC state to end up being `sendableToServer`.

I'm being pushy here because I still feel like it would pretty neat to have a "liberating" full & easy intermingling of CCs and SCs.

Also, I can still see using a stateful CC for conceptual routing, instead of using a new machanism, to be more React idiomatic. (I'm probably naiv here as I don't know much about Server Contexts.)

---

### #118 — @josephsavona — 2021-01-04 16:15

> One thing I was thinking is to forbid users to render stateful CCs on the server-side. Maybe this could solve the problem while staying user-friendly. I'll think about this.

@brillout Yup! This is part of why client components aren't rendered on the server (among several other reasons). The solution - while staying user-friendly - is the RFC here :-). Similarly, allowing developers to render server components directly from client components is problematic for a number of reasons (outlined above by myself and @gaearon - state serialization, waterfalls, etc). Ultimately, this would increase complexity of the proposal without providing new features that can't be achieved more powerfully via other means (routing integration, server context, etc), so this isn't something we plan to support.

---

### #119 — @Ephem — 2021-01-04 18:00

First, thanks for all the excellent work and effort you are putting into all the thoughtful answers and discussions here! ❤️

> Can you be more specific? Are we talking about SSR, or about Server Components (or how they work together)? The neat thing about Server Components is that you don't really need to serialize the cache itself because it's really the render output that you're after. The cache that runs on the client only caches server responses, but the data you've fetched on the server isn't even needed by the client. Only the rendered result.

This was an answer to @jamesknelson but since it's related I'll also comment. Hypothetically, what if it _is_ needed or you want to for some reason? I guess there are two separate things to discuss here, one is "Does there exist any scenario where it is desirable for a client side cache to be populated by data from Server Components?" and second is "How could that be done according to this RFC?".

> With the idiomatic Server Components model, you "pass" things by passing props to Client Components. Including refetches. Nothing more, nothing less. This is a different model than traditional normalized caches — it's denormalized. In this model, the client doesn't need the normalized data because you prepare the render result on the server.
> 
> It's hard for me to comment in more detail unless you expand on this point with a more specific scenario. But broadly speaking, Server Components don't require transferring the server cache to the client.

Just to be clear, I'm not necessarily talking about normalized vs denormalized here, but rather "How do I get the props a child component receives from a Server Component into an external cache, given that they need to be in that cache on the same render to avoid mismatches?".

To better describe the problem, I'll try to describe a decently simple scenario rather than one that necessarily motivates why this is important. So for now I'll leave the desirability aside for better focus, I'm happy to discuss that too of course, just want to make sure we are on the same page about the challenge first since it is pretty involved. 😄

**Scenario**: I want to have a single top level SC for each page that fetches my data, but _for reasons_ I want to avoid a lot of composition and interleaved Server and Client components, so rest of the page is just client components, which I also render via SSR on initial request.

Say one page presents a paginated list of books the user has liked. So we need to first fetch the user and then this list (waterfall), but when paginating, we only have to fetch the next page of the list. When navigating to this page, the SC avoids a Server->Client waterfall by fetching both, but _for reasons_ I want that paginated list to be a Client Component and fetch that data in a traditional way, using some library that is using an external cache.

In other words, I want to pass (at least some part) of the data from the SC into a separate abstraction for later use. This needs to also work for the initial SC->SSR->Hydrate case, which means it needs to be passed into that separate abstraction both on SSR and the Client. If the only way we have access to that data is via props in render, and we have no safe way of passing props into an external cache inside of render:

* _No_ usecase where you want to pass data from SC into a "client side" abstraction will work
* _Unless_ that abstraction only uses props/React context (since you can put stuff on context inside render)

The point you can pre-populate an external cache safely _without_ SCs is before the SSR on the server and before the Hydration on the client so it's already there when rendering, but with SCs it's trickier.

Maybe the answer is "_Because of the intersecting constraints of Concurrent Mode and SCs being able to refetch, there is no possible safe way to pass props into an external cache before SCs re-render or at render, so any abstraction that wants to take over/use/consume SC data needs to only rely on props or React context_"? That's fine of course, but most libs today does not conform to that which is why I'm trying to dig into this. Or maybe this will be solveable somehow with Suspense and a new async server renderer and hydration?

I guess a hypothetical solution could be a new lifecycle event that happens once before a Client Component re-renders because of new props from a SC? A safe `componentWillReceivePropsFromSC` if you will. 😉

Am I making sense in describing the problem as I see it? Maybe you were rather saying "We don't think there is _any_ usecase where an abstraction should take over SC data on the client" and were rather asking for valid use cases?

---

### #120 — @josephsavona — 2021-01-04 18:59

@Ephem The use-case you're describing sounds similar to a situation we've faced internally. In our specific example, Server Components may need to load Relay data for the Client Components that they render and somehow pass that data down to the client and stored in Relay store (ie, a non-React store) prior to the client component rendering. We currently achieve that by passing that data in a side channel - we are embedding the Server Component response within a GraphQL response, so we store the data for the child Client Components in that same GraphQL response and process it before rendering the Server Component response. 

I'm describing the above in the interests of transparency: Server Components are not and will not be coupled to GraphQL or Relay in any way, that's just an example to demonstrate that we have the same use-case you describe and are continuing to evaluate how to approach this generally.

---

### #121 — @Ephem — 2021-01-04 19:16

@josephsavona Spot on! So instead of embedding/extracting data from the "SC channel/payload", you are embedding SC output in the data channel, very interesting, thanks for sharing!

Without knowing details, my spontaneous thought is that having it that way around would make it hard for libs since it seems to require pretty deep integration and owning the layer around the app? Either way, this isn't something that needs figuring out here and now, I'm happy just to hear acknowledgement of the use case and that it's something that (might) need more investigation. 👍

---

### #122 — @brillout — 2021-01-04 19:19

@josephsavona

Thanks for your answer :-).

> state serialization

See my comments about
 - The sandwich approach https://github.com/reactjs/rfcs/pull/188#issuecomment-753645129
 - The `sendableToServer` option for `useState` https://github.com/reactjs/rfcs/pull/188#issuecomment-753818715

These solve the problem about heavy or unserializable states.

> for a number of reasons

Which are? :-)

Beyond waterfalls and heavy/unserializable state (which I both addressed), I don't see any problem.

> The solution - while staying user-friendly - is the RFC here

Wouldn't you agree that managing a conceptual route with a stateful CC is simpler and more idiomatic than using an entirely new mechanism?

I do see Server Contexts to be a solution but I don't see it to be simpler. There may be advantages about Server Contexts I'm not seeing as I only have information about Server Contexts through what Dan wrote here.

But, most importantly, why having a limiting restriction that CCs aren't allowed to import SCs if we don't have to?

We can also have both: Server Contexts (I actually quite like idea of explicitely defining state shared between client and server) *plus* my propsal.

I don't see any problem with my propsal that is not fixable. I'm more than happy to be shown wrong :-).

One way to think about my proposal is to liberate users from doing whatever they want, while the waterfall problem is solved by:

> While rendering the app tree, when a branch goes server-side, it never goes back client-side

This completely adresses the waterfall problem. (I've thought a lot about this; I'm getting confident about this.)

---

### #123 — @gaearon — 2021-01-04 19:46

>Hypothetically, what if it is needed or you want to for some reason? I guess there are two separate things to discuss here, one is "Does there exist any scenario where it is desirable for a client side cache to be populated by data from Server Components?" and second is "How could that be done according to this RFC?".

Thanks for explaining, that makes sense. So in the default "idiomatic" data fetching you would not need it because the client would just render the output — _but_ as you're saying there are cases where it might make sense to populate some kind of a cache. Like @josephsavona said, _we_ currently do this with Relay, but we could also extend the Server Components transport protocol to support emitting additional data that's consumed by some client cache. This would be out of scope of this RFC but is not contradictory to it.

>having it that way around would make it hard for libs since it seems to require pretty deep integration and owning the layer around the app? 

I don't think I understand how this would be significantly different from the integration people have to do today, where they often need to run some kind of an (unsupported) "prepass", and then stick the resulting JSON into the page so it's wired up later. This seems similar except that you benefit from streaming. But yeah, this is a follow-up use case, similar to how we'll need to figure out what CSS solutions should do.

---

### #124 — @Ephem — 2021-01-04 20:20

> So in the default "idiomatic" data fetching you would not need it because the client would just render the output

I very much agree with and like this idiomatic solution btw. I think this use case might be especially important for existing apps and migrations.

> but we could also extend the Server Components transport protocol to support emitting additional data that's consumed by some client cache. This would be out of scope of this RFC but is not contradictory to it.

Sounds good. I could see ways props would still be that medium as long as you could "receive" them before render somehow, but might very well require/make sense as "its own thing" as well. I guess this might come down to component level vs app level?

> I don't think I understand how this would be significantly different from the integration people have to do today, where they often need to run some kind of an (unsupported) "prepass", and then stick the resulting JSON into the page so it's wired up later. This seems similar except that you benefit from streaming. But yeah, this is a follow-up use case, similar to how we'll need to figure out what CSS solutions should do.

Yeah I'm not against having something "outside of React" that does this (receive the data from SC for example), that might be the right place. What I'm thinking is that if in order to get data from SC to an external cache(/thing) you need to reverse and embed SC in a data layer that sounds a bit awkward and also more like a framework level solution rather than a library one. I'm excited for SC as the transport layer. To use a bad analogy, in a future world were both supported SC, if you wanted to use Apollo in one part of the app, and React Query in another, how could you do that if it's required that SC is embedded inside one of those data payloads?

(This is no bash on your internal solution of course, that sounds like a great solution for your case as well as this point in time.)

But these are premature details, now that I know it's on your radar I'm confident you'll figure out a good solution when it's time to explore that further! 😍

---

### #125 — @lilactown — 2021-01-05 01:21

What's the story for doing authorization on the server side? It's not clear to me how to get the user's context (e.g. via an authorization header in the request) so that I can identify and authorize whether they should see what they have requested. Is there some place in this RFC that should be?

---

### #126 — @gaearon — 2021-01-05 01:27

@lilactown Is there any reason you’d expect authorisation to work differently from how you’d authorise API calls today?

---

### #127 — @sergiodxa — 2021-01-05 01:50

@gaearon I think the main doubt about auth is how we can know the current logged-in user from **inside** a SC. Imagine I need to get a list of todos but I should only get my todos, how can I let the fetcher or DB query function know my current user? I understand that I could add a layer of auth to check if the user is logged-in and reject the request before rendering the SC but then how could I get the request object and extract the auth token. I imagine doing something like this:

```js
function TodoList() {
  const request = useHTTPRequest() // this is what needs to be available for SC, maybe useServerContext should do the trick here
  const token = getAuthToken(request) // read from cookie or header, doesn't matter
  const todos = fetchTodos(token)
  return <section>{todos.map(todo => <Todo key={todo.id} {...todo} />)}</section>
}
```

---

### #128 — @lilactown — 2021-01-05 01:56

In most projects we handle authorization at the route level, e.g. some middleware looks up the users ID based on an authorization header and turns that into a set of capabilities. Routes can statically declare what capabilities are required in order to work, else respond with a 401. Routes can also receive a list of capabilities and determine behavior based on them.

So if I extrapolate from my past experience and read this part of the RFC:

> [framework] The framework’s router will match the requested URL to a Server Component, passing the route parameters as props to the component. It will ask React to render the component and its props: in this case, Note.server.js.

Then I can infer that the framework is responsible for authorization: taking the header, resolving the user's ID and capabilities and passing those as props. The framework is also in charge of creating some idiom for declaring authorization for components, e.g. no one without `admin` privilege should see the `AdminPanel` component.

The things that I'm left wondering are:
* What does the user see if the app requests a component that fails for some reason (401, in this case)?
* if I use Context to pass around the user info (e.g. user ID) on the client, could I use the same abstraction in a server component? E.g. could the framework provide the user ID and capabilities in some way where I could write a shared component like:

```javascript
function UserProfileList() {
  let { userId, capabilities } = useContext(UserContext);
  if (capabilities.includes('admin')) {
    // render user list with edit delete button for all users
  } else {
    // render user list with only edit button for themselves
  }
}
```

So to bring this back to the RFC, I suppose my actual questions are the two above. What does a rejection or error look like when requesting an SC, and would it be possible for a framework to provide context to a component the same way a parent component can provide context to a child component?

---

### #129 — @wmertens — 2021-01-05 08:08

In light of the recent comments, I would like to see the data side channel be part of the RFC.

I'm imagining something like a hook that SC can call during render, which emits the data in the stream, and an onData callback (or async generator) on the client side to consume the stream.

Probably this also needs some server-side scratch space to keep track of sent data between async render calls.

Then a current SPA with Apollo can get streaming SSR  by using the data channel to populate the client side cache, and the CC simply consume the cache.

---

### #130 — @josephsavona — 2021-01-05 14:59

@brillout Since this discussion got a bit spread out I’ll coalesce answers from @gaearon and I here. 

### Why Disallow Importing Server Components From Client Components?

As background, these types of constraints are actually very freeing. It’s generally much easier to lift a constraint later than to add a constraint you didn’t foresee or thought you could get away without. If, for example, it were the case that allowing Client Components to import Server Components turned out to be problematic — slowing down development (or performance) of React, enticing apps into problematic patterns, etc — then it could be harmful to the entire ecosystem while also being difficult for us to resolve. Therefore we have a high bar for adding features to React. We prefer to start with a well defined, well understood core set of features and expand them based on insights from using the core features in practice more widely.

With that in mind, note that allowing Client Components to directly import Server Components is a purely additive capability relative to the features proposed in this RFC. Allowing this capability wouldn’t allow us to simplify the implementation of Server Components. In fact the opposite is true: it makes the implementation and integration more complex.

Among the points we’ve considered here:

* One of our goals with Server Components is to give developers a powerful, easy-to-use tool for *avoiding client/server waterfalls*. We already support *loading* Server Component output from a Client Component - note that in the demo the root of the app is a Client Component. Allowing client/server waterfalls is more than a non-goal: we’re trying to get as close as we can to making it easier to avoid such waterfalls than it is to create them (allow developers to fall into the performance “pit of success”).
* With that in mind, the only way we would consider allowing Client Component to import Server Components is if we did so in a way that avoids client/server waterfalls. This naturally leads to something along the lines of [@brillout’s proposal](https://github.com/reactjs/rfcs/pull/188#issuecomment-751797544), where:
    * A Client Component (CC) importing a Server Component (SC) causes (via bundler magic) a stub to be imported that fetches the SC on demand.
    * Server Components have to fully render their Client Component leaf nodes just in case there are nested Server Components. Not doing so would allow client/server waterfalls.
* First, note that this approach requires many of the *same* architectural components as the RFC:
    * It motivates a concurrent-compatible caching mechanism to cache the results of Server Components.
    * Developers would still want routing and framework integrations.
    * We still need bundler integrations so that Server Components can dynamically choose Client Components.
    * etc
* Second, note that this approach requires *additional* complexity beyond what is necessitated by this RFC:
    * It requires an additional bundler integration to allow Client Components to import stubs of Server Components.
    * It requires some mechanism for React *itself* to fetch the results of a Server Components and render it, as opposed to that being an application/framework-level concern. In the proposal linked above, for example, React itself would have to call a `/_react/render` endpoint that was responsible for rendering the SC tree. But calling an endpoint requires users injecting some mechanism to make this request, possibly a convention for the endpoint address, etc. 
    * It requires serializing potentially massive amounts of state from the client to the server for each request. 
    * It doesn’t guarantee no client/server waterfalls, as it will always be possible for state to change on the client such that a different branch of the UI is rendered, which the Server + Client tree rendered on the server didn’t pre-populate data for.
* Finally, having to *always* render Client Component children on the server (as opposed to this being opt-in with Server Components plus SSR) is problematic for a few reasons:
    * Ideally developers would be allowed to reference truly client-only APIs in their Client Components - ie not all Client Components should have to be executable on the server at all.
    * It increases the amount of work the server has to perform by default.


Given the above, we do not plan to include support for importing Server Components from Client Components in the initial version of this feature. This is something we are not completely ruling out, though, and we *may* consider in the future.

---

### #131 — @brillout — 2021-01-05 18:25

@josephsavona

Thanks for the elaborate answer, it makes a lot of sense.

I had an epiphany of why the contraint of forbidding CCs to import SCs would be better than my proposal:
1. The constraint naturally leads app developers to move logic to the server. This eventually turns CCs into "dumb" stateful components. This is a good thing: the goal of SCs is to move stuff to the server, and incentivizing the move of logic to the server aligns well with the overaching goal of SCs.
2. CCs can actually still be *easily* integrated at any level. The thing here is that because of 1. most logic end up living on the server-side, and adding a CC at any level is just a matter of "squeezing" the CC into the SC tree.
3. CCs interact with SCs in a seamless way with Server Contexts.
4. Server Contexts makes defining state that is shared between client and server explicit and precise. (My solution `sendableToServer` is a much more coarse way of doing it.)

I'm exicted to try out SCs *with* the constraint :-).

From my perspective, my propsal is now closed.

Thanks for the interesting discussion and for pushing the envelop. You are laying the foundation not only for React, but for any future interactive thin client which will take inspiration from your work.

Thanks.

---

### #132 — @gaearon — 2021-01-05 18:32

>I think the main doubt about auth is how we can know the current logged-in user from inside a SC. 

Sorry if I'm being dense but I'm still struggling to tell how this is different from how you'd write any API call. You could do the check before passing control into React, because you're on the server. Similarly, just like with any API call, you could obtain the user and do arbitrary checks, and throw if the conditions are not valid. Any errors you throw would be propagated to the client, where they would be handled by the closest Error Boundary, similar to errors thrown inside components in general.

>In light of the recent comments, I would like to see the data side channel be part of the RFC.

We'd like to not commit to something as extensible at this point in time. We may add something, but it doesn't directly affect this RFC in particular, and we need to be very careful about how this works so we think it's too early to figure out.

>Then a current SPA with Apollo can get streaming SSR by using the data channel to populate the client side cache, and the CC simply consume the cache.

Server Components require a lot more considerations to work out, including routing, refetching, etc. So it is premature to think about how a "current SPA" can be ported to them. They have important implications on architecture and aren't exactly drop-in.

---

### #133 — @flybayer — 2021-01-05 21:25

> Exciting proposal! Good work everyone!
> 
> My only request is please use a serializer like [`superjson`](https://github.com/blitz-js/superjson) which supports serialization for `Date`, `undefined`, `BigInt`, `Map`, `Set`, etc in both directions. [`devalue`](https://github.com/Rich-Harris/devalue) is another option but is only safe for server to client, not client to server.

There's been a few comments/requests about serialization without answer, so I wonder if you can speak to it?

Serialization of `Date`s is by far the most common case. If `Date`s are not allowed as props in some cases, it would be confusing and frustrating.

---

### #134 — @wmertens — 2021-01-05 21:30

As I understand it, the serialization will be performed by the framework.

Something like https://www.npmjs.com/package/@yaska-eu/jsurl2 (shameless plug) would be useful indeed ;)

---

### #135 — @mizdra — 2021-01-09 09:54

Thanks for the exciting proposal!

Is this a solution to Component Folding (https://github.com/facebook/react/issues/7323) ? As far as I can see, the Server Component and its mechanism is an approach that partially solves Component Folding by using runtime information in the server. Intuitively, I think the limitation of this approach is that it only folds the Server Component and not the Client Component. I would like to hear if you have any interesting insights on this issue 😃

---

### #136 — @eyelidlessness — 2021-01-09 18:08

Regarding serialization, I sincerely hope React won’t be prescriptive but instead allow developers to choose their own format, so long as it satisfies a common interface (eg the `JSON` API, as that’s what most people will probably default to). This would allow people to choose JSON5, YAML, EDN, Transit, whatever they need for their use case.

Aside: for those folks developing a richer serialization format, I highly recommend looking at prior art like EDN/Transit to see how they work. It’s great to build in additional native types like `Date`, but an extensible and namespaced format is a huge benefit for a lot of applications.

---

### #137 — @AlzAmido — 2021-01-11 15:02

**What about micro-frontends?** 
One of my clients is a very large organisation, implementing a very large e-commerce platform and we had to migrate away from NextJS (and write our own framework) because it was impossible to tell the client instance of NextJS to speak to different server (NodeJS) instances of NextJS (even with the Next Multi-Zones approach, which would work only if I had one MFE per route). 
This is because there are multiple React Apps running on the same page. Each App is SSR + Rehydration and they communicate through a custom service bus (eventing) system we wrote (based on RXJS and using custom hooks for subscriptions).
Will there be chances this type of architecture will be supported? I find the MFE architecture to have excellent results for large orgs which have large sets of artefacts and rely heavily on caching/regions so I am not ready to abandon the paradigm just yet but at the same time I feel Server Components could help simplify our architecture in the long run.

---

### #138 — @natew — 2021-01-11 23:57

Curious -

React really has two major concepts these days, Components & Hooks. This solution seems to work well for Components, but what about Hooks?

In your example, you have a DateTime formatting component that imports `moment` which is huge. But, we may want to use moment in other contexts, perhaps it's used to format something before we make an API call. Would it then be possible to do this?

```
<MomentFormatter date={new Date()} onFormattedDate={formatted => console.log(formatted)}
```

Or do React Server Components somehow prevent callbacks from the server? I'll have to read over it more. Basically, wouldn't it be nice to have *anything* be able to be put on the server? In a sense this would basically be like "serverless" at the code-level in React/bundlers.

So you could have, in `momentFormat.server.js`:

```
export function momentFormat() { ... }
```

And then if you wanted a hook in `useMomentFormat.server.js`:

```
export const useMomentFormat = (...args) => momentFormat(...args)
```

And if you wanted, a `MomentFormat.server.js` component. At least to me, this would be a really nice paradigm for serverless that would basically integrate perfectly with server components.

---

### #139 — @sergiodxa — 2021-01-12 00:03

@natew I think what you want is an API endpoint to send a date and get a formatted date with moment and a hook to fetch it

---

### #140 — @natew — 2021-01-12 00:09

@sergiodxa That's not what I'm asking.

Though after reading over the proposal, I can see server components are not stateful, so this wouldn't work within this paradigm. That said, avoiding having to make an API endpoint by just putting a pure-function in a `.server.ts` file would be far nicer than having to generate/glue together api endpoints for small functions.

---

### #141 — @sergiodxa — 2021-01-12 00:16

Indirectly, to make `momentFormat.server.js` work server-side you will to autogenerate an API endpoint and when importing it get a wrapper which fetch this API endpoint (so all your server functions would be async).

For `useMomentFormat.server.js` to work server-side you will need something similar, but this time you will get a wrapper hook which calls the "server hook" API endpoint and give you the result in an async way (undefined first, value later or suspending).

Something like this is supported by [Blitz.js](https://blitzjs.com) in case you want to take a look, it's really cool to automatically get API endpoints.

---

### #142 — @natew — 2021-01-12 00:23

@sergiodxa Yep, that's what I was proposing, though basically having it more baked into RSC. You could in theory apply the rules of RSC and have hooks work, but it would be weird in that you'd have to be careful to only use Suspense and no state.

Would love to use Blitz but Next.js doesn't play well with the stack/routing needed for mobile apps (you need a non-filesystem based routing approach, ideally), but thanks for the heads up, I'll look at the tech there and perhaps see what I can use as inspiration. Edit: also aware blitz supports non-file routing, but there are many reasons it's not a good fit still.

---

### #143 — @dan2k3k4 — 2021-01-12 13:36

I'm curious as to how React Server Components will impact the usage of [Loadable Components](https://loadable-components.com/)? The [React docs](https://reactjs.org/docs/code-splitting.html#reactlazy) suggests the usage of them for code-splitting.

---

### #144 — @josephsavona — 2021-01-12 14:59

@dan2k3k4 As noted in ["Automatic Code Splitting"](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#automatic-code-splitting), any Client Component that is rendered by a Server Component is automatically eligible for code-splitting and may be bundled separately, depending on the specific bundler's heuristics. There is no need to use `React.lazy` or a 3rd party library, this happens automatically.

---

### #145 — @roman-lezhnin — 2021-01-12 15:27

I saw the code in the presentation for which I am very ashamed) Request to the server from the ui component (data access layers and UI layer are mixed). Would it be possible to build a normal application architecture like MVVM or Clean architecture? Or will the UI communicate with the data base and file system?

---

### #146 — @dejanmilosevic0 — 2021-01-14 19:24

Is it possible to run react server components without webpack, but with snowpack and esm modules? It should be builder/bundler agnostic and even to have easy way to implement custom server without bundler, just with some module that creates react-client-manifest.json.

---

### #147 — @yeliex — 2021-01-15 02:06

any plan to production or release version?

---

### #148 — @Nilanth — 2021-01-16 12:40

Does this increase server cost?

---

### #149 — @andriiradkevych — 2021-01-16 14:19

I think it will slow down the first contentful paint results when we will use this approach. Am I right? Is there a possible way to save state in component by using rehydration approach, for example, I've got some data before rendering on SSR, and then when rehydration happens, save this data, and prevent sending a request on the client-side. In other words, pass data to client side from ssr 

https://redux.js.org/recipes/server-rendering


```
    <script>
          // WARNING: See the following for security issues around embedding JSON in HTML:
          // https://redux.js.org/recipes/server-rendering/#security-considerations
          window.__PRELOADED_STATE__ = ${JSON.stringify(preloadedState).replace(
            /</g,
            '\\u003c'
          )}
        </script>
        
```

above you can see the possible way, but it will be great to prevent all of this huck and have the opportunity to have this data directly 

```
  router.get('/home-page', ctx =>
    // prefetch data you need
    
    const data = fetch().json() or request to db doesn't matter
    
    return ReactDOMServer.renderToString(<Component data={data}  />)
  )
```
  
  **Components.js**
  ```
  const Component  = ({data}) => {
    const data  = useState(data)
    
    return <div></div>
  }
  ```
  
  and when rehydration will happens, useState will have data which you have got on ssr (some sort of initial data)

---

### #150 — @trm217 — 2021-01-28 06:38

> Does this increase server cost?

Obviously more processing on the server will lead to an increase in server-usage and thus in some cases, cost.
However, this might just be worthwhile since the data-transfer between server & client (which for many hostings is pricing related as well) would decrease, because of the smaller bundle size.

---

### #151 — @smikitky — 2021-02-03 02:30

Are class components supported on the server side? I tried to render the following `ClassComp.server.js` from `App.server.js`, and got a weird compile error.

```js
import React from 'react';

export default class ClassComp extends React.Component {
  render() {
    return <div>Hello, Class-ical Component!</div>;
  }
}
```

If I rename this to `ClassComp.client.js`, it works fine. Of course I understand no one will ever need this because SCs don't have state/lifecycles, but it may be worth mentioning this in the RFC if this is not supported.

---

### #152 — @gaearon — 2021-02-06 20:23

> I think it will slow down the first contentful paint results when we will use this approach. Am I right? 

No. I think you might be missing the fact that there will be a streaming HTML renderer that stays in the middle between React Server Components and the client. So for the first load we’d definitely avoid the additional roundtrip.

---

### #153 — @nick121212 — 2021-02-07 05:25

I think React Serer Component is an interesting thing. How to share components between servers is also need to considered. like this: ` Import ServerComponentA from  'http://localhost:3000/ServerComponentA'`

---

### #154 — @josephsavona — 2021-02-08 17:22

> What about debugging issues with the react components in development? (as the component processed in server side and response will be special format) will developers have any clue on where to debug and find cause?

We discuss this in the [Open Areas of Research section](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#open-areas-of-research) - we're actively exploring how to provide great developer tools for Server Components.

---

### #155 — @lukemcgregor — 2021-02-09 04:17

Very interesting research and concepts. 

I was just looking the RFC at and playing with the demo, one thing I noticed was that in the payloads for the server components there is a lot of duplication (specifically in J4 in the example app's first request, see diff below) , especially relating to lists. List template duplication I one thing that I find frontend frameworks are very good at reducing, eg sending a template and some raw data and then reconstructing it has lower transfer cost than sending down a pre-rendered document, gzip helps a lot with this but I suspect even in this example its going to be bigger than the sum of data and template).

Perhaps the template should be separated from the props within the payload to avoid duplicates, alternately transmit some kind of compiled templates to the client as part of the bundle as opposed to passing them in the data payload. On the demo example and my hacky napkin example below was about 7% compressed (60% uncompressed) in savings using a template, this is likely to be much worse on bigger lists.

![image](https://user-images.githubusercontent.com/1284608/107314957-a3f45880-6afa-11eb-9cd3-ef483e1b0a81.png)


```
{
    "data":[
        [
            [
                "It's very easy to make some words bold and other words italic with Markdown. You can even link to React's...",
                "Make a thing",
                "2/3/21"
            ],
            [
                "I wrote this note today",
                "It was an excellent note.",
                "3:47 AM"
            ],
            [
                "A note with a very long title because sometimes you need more words",
                "You can write all kinds of amazing notes in this app! These note live on the server in the notes...",
                "3:54 AM"
            ],
            [
                "Meeting Notes",
                "This is an example note. It contains Markdown!",
                "1/3/21"
            ]
        ]
    ]
    ,
    "template":[
            "$",
            "ul",
            null,
            {
                "className": "notes-list",
                "repeat": "data[0]",
                "children": [
                    [
                        "$",
                        "li",
                        "4",
                        {
                            "children": [
                                "$",
                                "@5",
                                null,
                                {
                                    "id": 4,
                                    "title": "data[0]",
                                    "expandedChildren": [
                                        "$",
                                        "p",
                                        null,
                                        {
                                            "className": "sidebar-note-excerpt",
                                            "children": "data[1]"
                                        }
                                    ],
                                    "children": [
                                        "$",
                                        "header",
                                        null,
                                        {
                                            "className": "sidebar-note-header",
                                            "children": [
                                                [
                                                    "$",
                                                    "strong",
                                                    null,
                                                    {
                                                        "children": "data[0]"
                                                    }
                                                ],
                                                [
                                                    "$",
                                                    "small",
                                                    null,
                                                    {
                                                        "children": "data[2]"
                                                    }
                                                ]
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                ]
            }
        ]
}
```

PS I know the above isn't a particularly elegant solution to templating, it was more to demonstrate the point on relative size using your existing structure so its apples with apples.

---

### #156 — @carrot-sticks — 2021-02-10 11:08

Can you please show us an example of this working with a list which will fetch new elements as user scrolls, preferably with some kind of windowing? 

I have a use case where we show big lists of components, and the user has some actions. To make things worse, those actions can disable the same actions on other list items. This now works by updating apollo cache, but will it ever work with server components?

---

### #157 — @josephsavona — 2021-02-11 15:28

@filipcro Pagination is an [open area of research](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#open-areas-of-research). We'll share more about these areas as we investigate them further.

---

### #158 — @samonxian — 2021-02-18 03:01

I didn't expect my idea to be so similar to the react team. I defined it as clientless, which has two characteristics **CaaS** (component as a service) and **interfaceless**.

- CaaS (Component as a Service)
   - Support protocol-driven rendering in Api mode
   - Support server side rendering (SSR) in UI mode
- Interfaceless (the interface display does not need to pay attention to the interface)
   - No need to write HTTP requests
   - Node does not need to define **UI API**
  
 **These two features are recommended for server components**  
   
**The server-side component is what we want, and we look forward to the server-side version update.**

At the beginning, we used the protocol-driven mode to control the rendering of the UI, but Node’s too many json object operations were very difficult to maintain. Clientless was proposed at the end of September 2020, and basic functions were supported at the end of October 2020. At the end of November 2020, I tried clientless on a project. Although it is rough, and better performance is not considered, the idea is feasible.   

Clientless is divided into 4 types of components:

- clientless component
  The clientless component is a front-end component that can be called on the Node side, similar to `xxx.client.js`.

- server component
  The server component **can only be called** on the Node side, which is consistent with `xxxx.server.js`.
  The following is the transfer method of clientless server components:
  ```json
  {
    "data": {
      "$type": "BindComponent",
      "$props": {
        "key": ".0",
        "shouldUpdateUrl": true,
        "reloadShouldSubmit": true
      },
      "$children": [
        {
          "$type": "ViewMutiModeSearch",
          "$props": {
            "key": ".0",
            "query": {
              "id": "430189080"
            },
            "data": {}
          }
        }
      ]
    },
    "msg": "jsx successfully converted to clientless protocol.",
    "responseId": "73c82d3b-d6f6-4050-80c4-aa8736d7c5db"
  }
  ```

- Bind component
  Special components are used to implement functions such as requesting node-side data from the front end and automatically updating URL parameters.

- Ordinary components
  It is the usual front-end component.

---

### #159 — @phuongnd08 — 2021-02-18 04:43

> Perhaps the template should be separated from the props within the payload to avoid duplicates, alternately transmit some kind of compiled templates to the client as part of the bundle as opposed to passing them in the data payload. On the demo example and my hacky napkin example below was about 7% compressed (60% uncompressed) in savings using a template, this is likely to be much worse on bigger lists.

I think the saving should be taken care at the server level (nginx gzip compression for example). I don't think we need to complicate this one for such gain.

---

### #160 — @lukemcgregor — 2021-02-18 04:49

> I think the saving should be taken care at the server level (nginx gzip compression for example). I don't think we need to complicate this one for such gain.

That's kinda my point, gzip isn't going to handle this well. See my test data relating to gzip, this is about the simplest example that you could have and even here your increasing payload by 7%. With more complex dom and more data this is only going to get worse.

---

### #161 — @wmertens — 2021-03-04 15:53

@lukemcgregor i think we'll see best practices evolve that include plumbing SC data down to CC for deduplication.

---

### #162 — @gaearon — 2021-03-24 16:08

There's been some questions about how streaming SSR would work. There's some initial description in https://github.com/facebook/react/pull/20970, if you're interested. We plan to release more in-depth content as this gets fleshed out.

---

### #163 — @tonynguyenit18 — 2021-03-27 04:49

Thank React team for great incoming feature, but I don't quite understand how Server Component help make data query faster?

Current data fetching: `client -> server (e.g: Restful) -> return data to client`
Server Component: `client -> Server Component Server (the server we host react app) -> server (e.g: Restful) -> return data to Server Component Server - > stream JSON of html to client`

If I'm right about the flow, I would say Server Component would be slower than normal Client React app?

---

### #164 — @gaearon — 2021-04-01 21:50

Today, we're [announcing](https://twitter.com/reactjs/status/1377731307929792522) React Labs — a new video series with technical deep dives with the React team members.

Our first video is a [Server Components Architecture Q&A](https://www.youtube.com/watch?v=jK0Vg8XbIXk&list=PLzIwronG0sE59zqnXPDDZ8qYuGPvHeJMA&index=2) deep dive. We hope you enjoy it!

---

### #165 — @miguel-silva — 2021-04-02 22:43

> Thank React team for great incoming feature, but I don't quite understand how Server Component help make data query faster?
> 
> Current data fetching: `client -> server (e.g: Restful) -> return data to client`
> Server Component: `client -> Server Component Server (the server we host react app) -> server (e.g: Restful) -> return data to Server Component Server - > stream JSON of html to client`
> 
> If I'm right about the flow, I would say Server Component would be slower than normal Client React app?

@tonynguyenit18 

For a single request and with that kind of architecture that is probably correct most of the time. 

But there are some scenarios where I can imagine Server-component based apps edging out pure Client React apps in data fetching, assuming that the **Server Component Server** is in the same infrastructure as the **RESTful server**:
1. A complex view that needs to fire off 2+ sequentially-dependent requests and then combine them in order to render something. This is due to roundtrips being much shorter between the servers than with the clients, and enabling only a single roundtrip between the client and the *Server Component Server*.
2. Big responses where only a small subset is actually needed to render a certain view. Again due to shorter roundtrip between servers, the **Server Component Server** would render and serve down to the client only the necessary payload.
3. A relatively static view that has medium/big sized dependencies which can run on server side. As exemplified in the Server components Demo (running a markdown renderer + dates lib on the server), one can offset a lot of the bundle size cost which the client would otherwise have to wait to be downloaded and parsed.

The most exciting premise for me with adopting Server components is that, as long as the base infrastructure for Server components is in place, there should be little cost in experimenting, measuring and switching as one sees fit between rendering something on the server or on the client.

---

### #166 — @tonynguyenit18 — 2021-04-03 23:17

> > Thank React team for great incoming feature, but I don't quite understand how Server Component help make data query faster?
> > Current data fetching: `client -> server (e.g: Restful) -> return data to client`
> > Server Component: `client -> Server Component Server (the server we host react app) -> server (e.g: Restful) -> return data to Server Component Server - > stream JSON of html to client`
> > If I'm right about the flow, I would say Server Component would be slower than normal Client React app?
> 
> @tonynguyenit18
> 
> For a single request and with that kind of architecture that is probably correct most of the time.
> 
> But there are some scenarios where I can imagine Server-component based apps edging out pure Client React apps in data fetching, assuming that the **Server Component Server** is in the same infrastructure as the **RESTful server**:
> 
> 1. A complex view that needs to fire off 2+ sequentially-dependent requests and then combine them in order to render something. This is due to roundtrips being much shorter between the servers than with the clients, and enabling only a single roundtrip between the client and the _Server Component Server_.
> 2. Big responses where only a small subset is actually needed to render a certain view. Again due to shorter roundtrip between servers, the **Server Component Server** would render and serve down to the client only the necessary payload.
> 3. A relatively static view that has medium/big sized dependencies which can run on server side. As exemplified in the Server components Demo (running a markdown renderer + dates lib on the server), one can offset a lot of the bundle size cost which the client would otherwise have to wait to be downloaded and parsed.
> 
> The most exciting premise for me with adopting Server components is that, as long as the base infrastructure for Server components is in place, there should be little cost in experimenting, measuring and switching as one sees fit between rendering something on the server or on the client.

Thanks @miguel-silva for your detailed answer.

---

### #167 — @bennettdams — 2021-04-08 13:58

> [We are planning to introduce a more granular refetching mechanism so that you have the option to refetch only a part of the screen.](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#are-you-always-refetching-the-whole-app-isnt-that-slow)

Can someone write down what exactly is planned to trigger a refetch of a Server Component? [The RFC only talks about what HAPPENS for a refetch](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#update-refetch-sequence) and right now [refetches are done via a full route switch](https://github.com/reactjs/server-components-demo/blob/main/src/NoteEditor.client.js#L39). 

___

Example: Initially a user visits some route and the framework knows that this route is associated to a Server Component. The Server Component gets data e.g. from a DB and the results are streamed to the Client. So far so good.
From this point on there are three very common use cases for the need of refetched data (aka. a refetched Server Component):

- interval
- mutations by the user (e.g. updating a blog post)
- events by the user (e.g. clicks on a button to show more data)

How would the Server Component/framework know how to refetch?
I don't think this topic is in the same area as [pagination or partial refetches](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#open-areas-of-research), as it is much more fundamental, because it applies to nearly all applications. 
[Looking at the RFC's example for mutation, it just skips this part](https://github.com/josephsavona/rfcs/blob/server-components/text/0000-server-components.md#basic-example):

```lang-tsx
  const submit = () => {
    // ...save note...    <<    Async request to save, but what comes after that?
  };
```

BTW: I think this is one of the reasons React Query got so popular, as it handles this topic really well.

---

Without full route switch, how does the Client Component let the Server Component/framework know that is has to refetch?

Maybe React could provide a first-class citizen hook to configure/control (re)fetch behavior via a Client Component?
**This hook would have to know a Child Component's parent Server Component** and e.g. executes a refetch.

```lang-tsx
  ...
  const { refetch } = useServer()
  ...
  const submit = () => {
    // ...save note...  
    refetch()
  };
```

---

### #168 — @gaearon — 2021-04-08 14:28

@bennettdams You might want to look at [the demo](https://github.com/reactjs/server-components-demo), which, among other things, [refetches after a mutation](https://github.com/reactjs/server-components-demo/blob/2d9fb948b7073f5f07e22d71350422ee9e1cc7f3/src/NoteEditor.client.js#L58).

---

### #169 — @adamkleingit — 2021-04-21 12:44

Have you considered allowing server components to have serializable state using a "cookie-like" mechanism?
Meaning you send the state with each request and the server uses it when rendering the components.
I think this can simplify the constraints, and avoid some of the use-cases of separating client and server components. Maybe also simplify the routing part because some stuff can just use the state (imagine you set a new state on a server component, it sends the state to the server and gets back a rendered subtree).

---

### #170 — @gaearon — 2021-04-21 15:11

>Have you considered allowing server components to have serializable state using a "cookie-like" mechanism?

It's been proposed somewhere earlier on this thread. This doesn't work generally — state in React is arbitrary, not necessarily serializable, and even if it were, the payloads could potentially get huge for the general case. This is what doomed ASP .NET WebForms, and we'd like to learn from their mistakes rather than repeat them.

The mechanism itself is useful though. That's how Server Context would be implemented. It's a special kind of context needed to implement routing and similar things. However, the use of that will need to be very limited, and it's not appropriate for generic arbitrary state.

---

### #171 — @adamkleingit — 2021-04-21 17:13

> > Have you considered allowing server components to have serializable state using a "cookie-like" mechanism?
> 
> It's been proposed somewhere earlier on this thread. This doesn't work generally — state in React is arbitrary, not necessarily serializable, and even if it were, the payloads could potentially get huge for the general case. This is what doomed ASP .NET WebForms, and we'd like to learn from their mistakes rather than repeat them.
> 
> The mechanism itself is useful though. That's how Server Context would be implemented. It's a special kind of context needed to implement routing and similar things. However, the use of that will need to be very limited, and it's not appropriate for generic arbitrary state.

Oh, sorry for the duplication, didn't see that one.
Actually, having state inside a server component doesn't make sense even if you enforce restrictions on it, because you can't pass callbacks to change the state, as they are not serializable 😅

---

### #172 — @brillout — 2021-05-04 06:52

I'd love to build a little experimental framework on top of:
1. RSC
2. [vite-plugin-ssr](https://github.com/brillout/vite-plugin-ssr) (do-one-thing-do-it-well SSR tool)
3. [Wildcard API](https://github.com/brillout/wildcard-api) (RPC implementation)

You said you don't want people to build frameworks on top of RSC. I guess because of its experimental nature; would it be ok if I publish it with a big notice that this is experimental and no one should ever use it in production?

Would love to play around RSC + SSR + RPC.

---

### #173 — @gaearon — 2021-05-04 16:30

Sure you’re totally welcome to experiment. Just keep in mind it’s not ready for production use, and a lot of internal wiring may change. Also keep in mind that we have a particular strategy for SSR (new streaming renderer that’s in active development and is partially available in the experiential releases). So you should probably dive into that too or you might get a wrong idea of how SSR is meant to be integrated.

---

### #174 — @Jarweb — 2021-05-07 12:43

If there is such an implementation，it will be very interesting:

```
function DemoServer ({id, children}) {
  const res = fetch(`http://a.com/content/${id}`).json()
  return children && children(res)
}

<DemoServer id={1}>
  {(res) => <DemoClient data={res} />}
</DemoServer>
```

something like "component as a service"

---

### #175 — @perilevy — 2021-05-09 14:20

@gaearon We learned that it's not recommended that function bodies would contain **side effects**, because it's part of the render phase which should be  **deterministic** (pure function, [see ref](https://reactjs.org/docs/strict-mode.html#detecting-unexpected-side-effects)).
Well in server components, it seems that data fetching requests can't be located inside a **useEffect** hook, otherwise they won't be **SERVER** components.

Then I wonder:
- whether server components should be pure.
- how shared components stick to those principles, unless you're going to perform forthcoming changes, maybe creating a new hook for server side effects (e.g server i/o).

---

### #176 — @theKashey — 2021-05-09 23:52

`deterministic` and `pure` are little different things. And for example - a function that always produces absolutely the same side effects can be named `pure`.

In the case of data fetching "ServerComponent" just operates in two different modes:
- there is no data, and it will fail. The function will be not executed, producing a side effect - loading the data.
- there is data, and it will pass. No side effects will occur in this case.

---

### #177 — @perilevy — 2021-05-10 06:47

@theKashey Maybe I misunderstood you, but http requests are side effects AFAIK.
Http request can fail due to many reasons, for example Network.
It depends on many things (e.g client connectivity, server availability).
I can also do the same for the "commit phase" and map all use-cases (e.g changes in DOM) and make it pure, according to you.

---

### #178 — @theKashey — 2021-05-10 07:32

> I can also do the same for the "commit phase" and map all use-cases (e.g changes in DOM) and make it pure, according to you.

This is how `useEffect` works - it _leaves_ an information record of what should be called, it "commit phase" does it.

It's all about abstractions. You can easily _fetch-mock_ your network request and _leave_ an information record of what should be fetched in the same way `useEffect` does. And look here - that would not change a single line in the actual application code. In this case - does it actually matter?

---

### #179 — @perilevy — 2021-05-10 08:37

@theKashey You are talking about whether it's testable, of course it's testable.
But it doesn't mean it's pure. `useEffect` is by definition a hook for side effects.
I suggest you to read again my first comment, I'm not talking about tests at all.
I also suggest you to read the [reference I attached about side effects](https://reactjs.org/docs/strict-mode.html#detecting-unexpected-side-effects) to understand why it's better to have a pure logic 
(hint: not just for tests).

A quote:

> it’s important that they do not contain side-effects. Ignoring this rule can lead to a variety of problems, including memory leaks and invalid application state. Unfortunately, it can be difficult to detect these problems as they can often be **non-deterministic**.

---

### #180 — @theKashey — 2021-05-10 08:58

You did not try abstract as I've asked. And I am not sure where you found "tests" in my message.
Note that API used in Server Components examples, as well as for Suspense render-as-you-fetch, is not "purely" `fetch`. It's some abstraction, with something like cache layer, and other strange things where you can ".fetch" data in one place and `.read` in another.

Well, instead of thousands words - https://github.com/reactjs/server-components-demo/blob/2d9fb948b7073f5f07e22d71350422ee9e1cc7f3/src/Note.server.js#L9

---

### #181 — @perilevy — 2021-05-10 11:54

@theKashey Well fetch-mock is a library for tests, probably a misunderstanding.
The cache layer doesn't make it pure, you can also read from fs, db, etc. as described in the talk. These all IO actions are side effects.
Even if we use a pattern, of injecting the data to cache in another place, it makes the server component a controlled component which waits for its provider data, and that provider component won't be pure.

---

### #182 — @gaearon — 2021-05-10 13:22

@perilevy 

>We learned that it's not recommended that function bodies would contain side effects, because it's part of the render phase which should be deterministic (pure function, see ref).

We're going to need to make this a bit more nuanced. Technically React components need not be strictly pure in the mathematical definition, but they need to be *idempotent*. This is what makes I/O possible, but only with very a limited contract which doesn't break idempotency. So React I/O libraries like `react-fetch`, `react-pg`, etc, will be allowed, because they will follow that strict contract (here is a temporary description before it gets into the docs: https://github.com/facebook/react/issues/17526#issuecomment-769151686). 

This still doesn't mean that you can do arbitrary I/O like actually running `fetch` or `fs` etc from your components. They must go through React wrappers that work with Suspense and follow that contract.

The idempotency requirement applies to both Server and Client components. There are no differences there. React I/O and Suspense would work exactly the same way on the client.

---

### #183 — @leaveLi — 2021-05-17 03:49

> If there is such an implementation，it will be very interesting:
> 
> ```
> function DemoServer ({id, children}) {
>   const res = fetch(`http://a.com/content/${id}`).json()
>   return children && children(res)
> }
> 
> <DemoServer id={1}>
>   {(res) => <DemoClient data={res} />}
> </DemoServer>
> ```
> 
> something like "component as a service"

CAAS, is fun😂

---

### #184 — @darren-at-shell — 2021-06-21 13:23

i still don't believe the exploit of serialisation has been addressed. If we are allowing for serialisable react components to be sent back from the server, then we cannot use the current security mechanism of providing "Symbols" to separate our user generated json "fake react structures" from real ones.

Ie the very old bug mentioned here - https://medium.com/dailyjs/exploiting-script-injection-flaws-in-reactjs-883fb1fe36c1

What is stopping someone crafting user input of the above style (albeit maybe slightly different now) like the following:

```
{
 _isReactElement: true,
 _store: {},
 type: "body",
 props: {
   dangerouslySetInnerHTML: {
     __html:
     "<h1>Arbitrary HTML</h1>
     <script>alert(‘No CSP Support :(')</script>
     <a href='http://danlec.com'>link</a>"
    }
  }
}
```

---

### #185 — @devknoll — 2021-06-23 20:07

> i still don't believe the exploit of serialisation has been addressed. If we are allowing for serialisable react components to be sent back from the server, then we cannot use the current security mechanism of providing "Symbols" to separate our user generated json "fake react structures" from real ones.
> 
> Ie the very old bug mentioned here - https://medium.com/dailyjs/exploiting-script-injection-flaws-in-reactjs-883fb1fe36c1
> 
> What is stopping someone crafting user input of the above style (albeit maybe slightly different now) like the following:
> 
> ```
> {
>  _isReactElement: true,
>  _store: {},
>  type: "body",
>  props: {
>    dangerouslySetInnerHTML: {
>      __html:
>      "<h1>Arbitrary HTML</h1>
>      <script>alert(‘No CSP Support :(')</script>
>      <a href='http://danlec.com'>link</a>"
>     }
>   }
> }
> ```

Can you elaborate what your concern is? React won’t render plain JSON objects (in modern browsers) — an element needs a `$$typeof` whose value is a symbol. The only way to generate that symbol is to run code on the client, and the only way the deserializer will do that is when it’s expecting to parse an element.

The only way (in the current implementation) it expects to parse an element is to read an array where element 0 is exactly the string “$”. The serializer won’t serialize a user string without escaping it, and any string that is exactly “$” is escaped as “$$” until it’s subsequently parsed and unescaped (as a string, not an element or symbol). And it will only serialize an exact string “$” when it is serializing an element — by checking that it has the symbol defined (which can only be set by executing code on the server).

---

### #186 — @brillout — 2021-07-27 16:20

I'm wondering how crawlers handle HTML streams? Do they wait until the HTML stream ends? In that case we could have SEO optimized pages with a fast TTFB. That would be a big deal. (I've created [StackOverflow - SEO/crawlability impact of HTML Streaming](https://webmasters.stackexchange.com/questions/136219/seo-crawlability-impact-of-html-streaming).)

---

### #187 — @wmertens — 2021-07-31 10:21

Caching results:

Would it be possible for each SC to indicate that it's cacheable with some key (via a hook) so that the result can be stored and immediately served when the same key is encountered?

The cache retrieval could happen before rendering. Based on the request, some cache keys are generated and if you find a fully matching set, you serve the page immediately.

---

### #188 — @jansivans — 2021-08-15 11:50

I have released initial implementation and docs for new server-side component framework Drayman - http://www.drayman.io/
It is not a substitute for React because it works differently and has other use-cases, but it also uses JSX syntax and some concepts are similar to React Server Components (like working directly with file system, databases, etc.), so I am here to help and provide info on how it was built and maybe something will become handy for this RFC.

---

### #189 — @brillout — 2021-09-22 20:10

Is there a plan regarding errors happening mid-stream? Imagine a page that is already 80% rendered but an error occurs in a React component in the last 20% of the HTML stream.

Seems like there doesn't seem to be a way to cancel/overwrite already sent HTML (but I didn't dig too much; I may have overlooked a solution).

I guess the only way is to have React overwrite the DOM to show the error page. But I wonder how the mechanics would work here. Seems like there need to be some (new?) API between React and the React framework (vite-plugin-ssr, Next.js, ...). There is [React Error Boundaries](https://reactjs.org/docs/error-boundaries.html) but I wonder how that would work with Server Components.

Is it something the React team has already thought about?

I'm currrently implementing HTML streaming support for [vite-plugin-ssr](https://vite-plugin-ssr.com/) (shameless plug :-)), and I'm super looking forward to add support for React Server Components.

Some prior discussion in the Marko community: https://github.com/marko-js/community/pull/1.

---

### #190 — @mikeposh — 2022-03-24 15:20

Perhaps using `isToday` from 'date-fns' (in the demo) is not a good example of something than can run on the server to save sending date formatting code to the client? 

The result of `isToday` for a fixed time will depend on the client's timezone, which won't be known on the server.

---

### #191 — @gaearon — 2022-03-24 19:25

Yes, it's not a perfect example.

---

### #192 — @lmatteis — 2022-10-17 12:33

How do you re-render a server-component (say you want to fetch new data) if it cannot be imported by a client-component (who would setState and change the server-component props)?

---

### #193 — @gaearon — 2022-10-25 02:00

Thanks everyone for the comments! We've made a number of changes in response to your feedback:

- [We've replaced the `.server.js` / `.client.js` filename convention with a `'use client'` directive](https://github.com/reactjs/rfcs/pull/227).
- [We've added native `async / await` support to Server Components](https://github.com/reactjs/rfcs/pull/229).

I've updated this RFC to link to those other RFCs with details. We're going to go forward with this as the first iteration.

---

### #194 — @penx — 2022-11-07 12:52

I've added SSR to the original demo:

https://github.com/penx/server-components-ssr

As we don't want the react-server codemod applied to the ReactDOMServer code, I'm running a separate worker thread with the codemod in it. I guess in production we could build out 2 applications (one with the codemod and one without) making this unnecessary, but it's fairly handy for development purposes! 

One thing I haven't figured out yet is how to deal with __webpack_chunk_load__ and __webpack_require__ on the server:

https://github.com/facebook/react/blob/8e2bde6f2751aa6335f3cef488c05c3ea08e074a/packages/react-server-dom-webpack/src/ReactFlightClientWebpackBundlerConfig.js#L75

https://github.com/facebook/react/blob/8e2bde6f2751aa6335f3cef488c05c3ea08e074a/packages/react-server-dom-webpack/src/ReactFlightClientWebpackBundlerConfig.js#L94

For these to work in ReactDOMServer I guess they need to be polyfilled?

---

### #195 — @apiel — 2023-11-28 11:33

I feel like RSC is missing a very important part of the developer journey with React. When we read the RFC, most of the example show how cool RSC is to fetch data directly from the database without the need to create an API in between. However, this is partially true, cause it is only the case on first rendering of the page (at the end very similar to SSR). However, if we want to load a new RSC from a client side component, "it's not really possible". If we follow the recommendation, this would enforce us to still use `fetch` to query an API in order to get dynamic data (or do some weird stuff with the application router...). Also, when looking at the server action, it is clearly mentioned that it should not be used to fetch data. Isn't react about interactivity? So why to limit RSC like this?

Being a bit frustrated by those limitation, I got over the recommendation boundary and did the following to use a RSC in a client component:

```tsx
"use client";

import { Suspense, useEffect, useState } from "react";
import { ServerComp2 } from "./ServerComp2";

export const ClientComp = () => {
  const [value, setValue] = useState<string | undefined>(undefined);

  // Use effect hook to fix Error: Server Functions cannot be called during initial render...
  useEffect(() => {
    setValue("demo");
  }, []);

  return (
    <div>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      {value !== undefined && (
        <Suspense fallback={<div>Loading...</div>}>
          <ServerComp2 value={value} />
        </Suspense>
      )}
    </div>
  );
};
```

and then my RSC:

```tsx
"use server";

import { readFile } from "fs/promises";

export const ServerComp2 = async ({ value }: { value: string }) => {
  // read tsconfig content
  const tsconfig = await readFile("tsconfig.json", "utf8");

  return (
    <div>
      My server component2 with val: {value} <code>{tsconfig}</code>
    </div>
  );
};

```

This way, I am able to load a "RSC" using server action, going against the recommendation saying that server action should not be used to fetch data as it doesn't have cache mechanism.
Why not to implement this cache mechanism so we could use RSC in a client component?

---

### #196 — @YYGod0120 — 2023-12-03 12:31

How to transform an application that is entirely composed of client components into a hybrid application with both client and server components? I hope our application will have better loading speed and performance.

---

### #197 — @apiel — 2023-12-03 12:39

> How to transform an application that is entirely composed of client components into a hybrid application with both client and server components? I hope our application will have better loading speed and performance.

@YYGod0120 if you are using nextjs have a look at https://nextjs.org/docs/pages/building-your-application/upgrading/app-router-migration or at https://www.youtube.com/watch?v=YQMSietiFm0

Even if in the tutorial they make it look like it is easy, in reality the transition for the SPA/SSR to RSC is not trivial at all, as you will have to completely rethink the architecture of your components...

If you are not using a "framework" like nextjs, it will be a big challenge to adopt RSC (at least for the moment).

---

### #198 — @YYGod0120 — 2023-12-03 13:04

> > How to transform an application that is entirely composed of client components into a hybrid application with both client and server components? I hope our application will have better loading speed and performance.
> 
> @YYGod0120 if you are using nextjs have a look at https://nextjs.org/docs/pages/building-your-application/upgrading/app-router-migration or at https://www.youtube.com/watch?v=YQMSietiFm0
> 
> Even if in the tutorial they make it look like it is easy, in reality the transition for the SPA/SSR to RSC is not trivial at all, as you will have to completely rethink the architecture of your components...
> 
> If you are not using a "framework" like nextjs, it will a big challenge to adopt RSC (at least for the moment).

Oh, that's unfortunate. My application doesn't use the Next.js. Perhaps I should consider restarting the entire application and creating a version 2.0.

---

### #199 — @flysky9981 — 2024-05-08 01:44

I read the demo of RSC, still have some questions:
1. which function or api is used to transform the RSC to JSON payload? is it the "renderToPipeableStream" method? or anything else?
2. where should I insert the SSR process? after the RSC JSON is generated and use this return value to do the SSR? then is there any dev tools to help me finish this ? 
3. it seems the "renderToPipeableStream" in react-server-dom-webpack and that in react-dom-server is not the same, the former generates the JSON RSC payload,but why both have the same function name?

---

## 코드 리뷰 코멘트 (42건)

### RC#1 — @swyxio — 2020-12-21 20:12
**파일**: `text/0000-server-components.md` L406

```suggestion
* **Pagination and partial refetches**. As noted above in [Update (Refetch) Sequence](#update-refetch-sequence), the typical method of reloading a page is to reload it in full. However there are some cases where this is not desirable, such as during pagination. Ideally our app would only fetch the next N items instead of refetching all items that the user has seen up to that point. We are still investigating how best to model pagination with Server Components. For example, internally we are loading Server Components via GraphQL, and using our existing infrastructure for pagination in GraphQL to work around lack of pagination in Server Components. However, we are committed to developing a general solution within React for this use-case.
```

---

### RC#2 — @wongmjane — 2020-12-21 21:37
**파일**: `text/0000-server-components.md` L367

```suggestion
    * ❌ *May not* use server-only data sources.
```

---

### RC#3 — @lucasecdb — 2020-12-21 21:40
**파일**: `text/0000-server-components.md` L451

```suggestion
No, they’re complementary. SSR is primarily a technique to quickly display a non-interactive version of *client* components. You still need to pay the cost of downloading, parsing, and executing those Client Components after the initial HTML is loaded. 
```

---

### RC#4 — @josephsavona — 2020-12-21 21:55
**파일**: `text/0000-server-components.md` L367

Thanks!

---

### RC#5 — @josephsavona — 2020-12-21 21:55
**파일**: `text/0000-server-components.md` L451

Thanks!

---

### RC#6 — @josephsavona — 2020-12-21 21:55
**파일**: `text/0000-server-components.md` L406

Thanks!

---

### RC#7 — @marceloadsj — 2020-12-22 09:15
**파일**: `text/0000-server-components.md` L292

A small fix, the note/text prop seems wrong:

```javascript
function NoteWithMarkdown({note}) {
  const html = sanitizeHtml(marked(note.text));
  // ...
```

(Or the consumers of NoteWithMarkdown should pass text={note.text} instead of the entire note={note}.

---

### RC#8 — @c0b41 — 2020-12-22 09:40
**파일**: `text/0000-server-components.md` L202

```suggestion
    return <OldPhotoRenderer {...props} />;
```

---

### RC#9 — @c0b41 — 2020-12-22 09:40
**파일**: `text/0000-server-components.md` L225

```suggestion
    return <OldPhotoRenderer {...props} />;
```

---

### RC#10 — @albannurkollari — 2020-12-22 14:05
**파일**: `text/0000-server-components.md` L292

Or just spread the `note` prop:
```js
<NoteWithMarkdown {...note} />
```

---

### RC#11 — @albannurkollari — 2020-12-22 14:11
**파일**: `text/0000-server-components.md` L72

Maybe `&&` instead of ternary statement:
```suggestion
      {isEditing && <NoteEditor note={note} />}
```

---

### RC#12 — @srflp — 2020-12-22 14:36
**파일**: `text/0000-server-components.md` L72

I'd leave it as it is, ternary operator is safer than AND operator in some cases.
Explanation here: https://kentcdodds.com/blog/use-ternaries-rather-than-and-and-in-jsx
tl;dr: It's easier to just use ternary operator because you don't need to think about the cases when the AND operator doesn't work as expected.

---

### RC#13 — @cangoektas — 2020-12-22 14:49
**파일**: `text/0000-server-components.md` L256

This has been a source of confusion for me. Server Components are praised as a solution to the waterfall problem when they would only (as of right now) minimize the symptoms of it. The talk mentioned that Facebook has solved this with Relay and GraphQL fragments, but it's not clear to me how Server Components would lead to no waterfalls as this section is titled.

Could you clarify how Server Components could be used to address the waterfall problem? I'm guessing that the team has some ideas, and it would be helpful to understand what part Server Components would play in them. It would also be interesting to understand how the waterfall could be solved in a non-Relay and non-GraphQL environment.

---

### RC#14 — @phryneas — 2020-12-22 14:54
**파일**: `text/0000-server-components.md` L256

I think the takeaway is that a server-side waterfall is much less problematic than a client-side waterfall due to much lower latency.

---

### RC#15 — @josephsavona — 2020-12-22 15:30
**파일**: `text/0000-server-components.md` L256

Yup, this is about moving round trips to the server so that you avoid the client-to-server latency.

---

### RC#16 — @josephsavona — 2020-12-22 16:27
**파일**: `text/0000-server-components.md` L72

Boolean short-circuiting w `a && b` evaluates to the value of `a` if that value is "falsey". Ternary expressions make it clear what the result is if the condition is false. We don't want to render `false`, we want to render nothing.

---

### RC#17 — @josephsavona — 2020-12-22 16:27
**파일**: `text/0000-server-components.md` L225

Thanks, will include this in an update

---

### RC#18 — @josephsavona — 2020-12-22 16:29
**파일**: `text/0000-server-components.md` L292

Thanks!

---

### RC#19 — @Daniel15 — 2020-12-22 18:25
**파일**: `text/0000-server-components.md` L230

Maybe change this to "No Client-Side Waterfalls" to make it clearer?

---

### RC#20 — @gaearon — 2020-12-22 18:29
**파일**: `text/0000-server-components.md` L230

Fixed.

---

### RC#21 — @acutmore — 2020-12-23 11:21
**파일**: `text/0000-server-components.md` L367

It could be helpful to re-mention here that client components can fetch and render a server component response.

---

### RC#22 — @eps1lon — 2020-12-23 15:22
**파일**: `text/0000-server-components.md` L359

Should we explicitly mention that `createContext` isn't supported yet? Server context as a missing feature is only mentioned in the FAQ right now.

Edit: Now that I think about it: The `react-server` entrypoint for `react` exports `useContext` but not `createContext`. Is `createContext` just missing or should `useContext` not be a part of the `react-server` entrypoint

---

### RC#23 — @eps1lon — 2020-12-23 15:22
**파일**: `text/0000-server-components.md` L360

```suggestion
    * ❌ *May not* use rendering lifecycle (effects). So `useEffect()`, `useLayoutEffect()` and `useImperativeHandle` are not supported.
```

---

### RC#24 — @gaearon — 2020-12-23 15:48
**파일**: `text/0000-server-components.md` L359

The plan is to have a distinct concept that `useContext()` reads on the server, like `createServerContext` or something.

---

### RC#25 — @gaearon — 2020-12-23 15:54
**파일**: `text/0000-server-components.md` L359

That would need to be its own separate RFC because there are some tricky considerations there that are out of scope of this proposal.

---

### RC#26 — @eps1lon — 2020-12-23 15:59
**파일**: `text/0000-server-components.md` L359

Should we remove `useContext` in the meantime from https://github.com/facebook/react/blob/50393dc3a0c59cfefd349d31992256efd6f8c261/packages/react/unstable-shared-subset.experimental.js#L17 to avoid potential confusion?

---

### RC#27 — @josephsavona — 2020-12-23 18:19
**파일**: `text/0000-server-components.md` L359

@eps1lon As noted by @gaearon, the idea is to eventually have a distinct API for contexts on the server that could be consumed with `useContext()`. While we're in the design phase of this, though, we've found it useful to still allow calling `useContext()` from Server Components. It's helpful for experimenting with server context approaches locally and also allows us to do a very simple "polyfill" of the eventual server contexts feature for our first production integration.

---

### RC#28 — @brunomoutinho — 2020-12-27 15:35
**파일**: `text/0000-server-components.md` L277

The part `AOT optimizations don’t work because they either don’t have enough global knowledge or they have too little.` seems redundant to me. If they don't have enough global knowledge, they do have too little global knowledge, so this should not be an `or`. Actually shouldn't be there at all.
I think just stating `AOT optimizations don’t work because they don’t have enough global knowledge.` is enough.

---

### RC#29 — @josephsavona — 2020-12-27 22:17
**파일**: `text/0000-server-components.md` L277

Good catch, I meant to write “...or they have too much”.

---

### RC#30 — @Ephem — 2020-12-28 19:19
**파일**: `text/0000-server-components.md` L364

```suggestion
    * ✅ *May* render other Server Components, native elements (div, span, etc), or Client Components.
    * ❌ *May not* pass props that are unserializable, like functions, to native elements or Client Components.
```

This is mentioned elsewhere in the RFC, but since this is a nice terse list of constraints, I think it makes sense to re-iterate this here?

I'm not sure how to best formulate it though, it's nice that the "May nots" come before the "Mays", but also makes sense that this follows the "May render" part which is why I included it there in the suggestion. 🤷

---

### RC#31 — @resynth1943 — 2020-12-28 22:21
**파일**: `text/0000-server-components.md` L45

Too much repetition here. It would be better to say 'Server Components' once, then leave it at that.

---

### RC#32 — @resynth1943 — 2020-12-28 22:22
**파일**: `text/0000-server-components.md` L111

```suggestion
*Client Components are just regular React components.*
```

Repetition.

---

### RC#33 — @resynth1943 — 2020-12-28 22:24
**파일**: `text/0000-server-components.md` L590

```suggestion
### Why not Rx?
```

Extra space here btw

---

### RC#34 — @resynth1943 — 2020-12-28 22:25
**파일**: `text/0000-server-components.md` L36

Did you mean to repeat this twice?

---

### RC#35 — @josephsavona — 2020-12-29 01:36
**파일**: `text/0000-server-components.md` L45

No thanks. Grammatical errors we’ll fix but this is purely stylistic / personal preference.

---

### RC#36 — @josephsavona — 2020-12-29 01:36
**파일**: `text/0000-server-components.md` L36

Yes.

---

### RC#37 — @resynth1943 — 2020-12-29 02:35
**파일**: `text/0000-server-components.md` L590

@josephsavona this isn't a gramatical error. I'm not going to argue with you to fix this, but it does seem to be a typo. :sweat_smile:

---

### RC#38 — @fdaciuk — 2021-03-04 10:24
**파일**: `text/0000-server-components.md` L72

Forcing `isEditing` to be a boolean value will bring the same result as ternary, but cleaner: 

```
{!!isEditing && <NoteEditor note={note} />}
```

But I think it's personal preference. Don't bother yourself about that :)

---

### RC#39 — @Ephem — 2021-03-13 22:37
**파일**: `text/0000-server-components.md` L326

> plus a bundle reference to the code for the component. 

Does this mean client code will always start downloading later than today? While you get to "initial paint" sooner because you don't have a code->data waterfall, this RFC seems to introduce an inverse waterfall of this in a sense where you need to get some data back before starting to load code? It's a nicer waterfall because you'll get _all_ the chunks you need to load back faster, even nested ones as long as they are generated by SCs, you get it fast because it's streamed on discovery and you have some initial things to show (the initial SC), but it still seems like a waterfall and affected by poor latency?

To avoid this, I guess frameworks/developers would have to start preloading any _known_ chunk(s) at the time you request a Server Component? Maybe some bundler support here would be possible? This info would need to be known ahead of time though which would bloat the bundle, so might not always be worth it.

I still think this is a lot better than the status quo, but I'd be super interested to hear more reasoning about these tradeoffs, seems like the RFC is glancing over this part a bit?

---

### RC#40 — @josephsavona — 2021-03-15 14:12
**파일**: `text/0000-server-components.md` L326

Yes! You're correct that depending on how things are implemented, a client _might_ end up starting to download client bundles later than they would have prior to Server Components. However, it's important to keep in mind that:
* In general, clients would have less code to download
* Applications and frameworks can choose to make tradeoffs where they preemptively send down information for some client bundles that are likely to be used. This is something that frameworks can automate via static analysis, runtime profiling, or a mix of both.

The key observation is that Server Components encode the required set of client components precisely, allowing the framework to help make choices about how to optimize delivery of those components.

---

### RC#41 — @Ephem — 2021-03-15 15:58
**파일**: `text/0000-server-components.md` L326

With _always_ I meant and should have said _unless you specifically address it in userland_, and it's definitely a small tradeoff to make for all the gains you get! Even without going the extra mile to implement preloading of code, I think this would only really hurt compared to today in some specific scenarios?

* You have a "thin" Server Component at the top (the elements you get back for immediate insertion into the DOM aren't immediately useful to the user) AND
* Most of your other components are Client Components (so you don't save much payload) AND
* You have a high latency scenario, so the extra time before code download starts hurts

As you say, because SCs encode the required Client Components precisely you have a better starting point than before if you choose to address this in userland. 

Albeit minor, this does seem like the only "fundamental" tradeoff SCs makes compared to today and it wasn't immediately obvious to me that there were _any_ scenarios where "vanilla" SCs could possibly perform worse than the status quo.

As someone who plans on implementing SCs from the low level primitives I found it interesting to realize this was a non-trivial problem I'd need to think about and tackle in userland which is why I thought I'd mention it. 😄

---

### RC#42 — @wantyouring — 2021-07-25 17:19
**파일**: `text/0000-server-components.md` L555

The content below is that even if the parent Client Component is refetched, the child Server Component is not re-rendered. 
So I think that the title should be like this, 
`Are Server Components refetched whenever their parent Client Components re-rendered?`.
I understood that Server Components should refetched when their props changed.

---

## 리뷰 (3건)

### @resynth1943 — COMMENTED — 2020-12-28 22:28

Just a few suggestions / questions.

---

### @gkannan1989 — COMMENTED — 2021-02-06 20:33

> ### What is the response format?
> 
> It’s like JSON, but with “slots” that can be filled in later. This lets us stream content in stages, breadth-first. Suspense boundaries mark intentionally designed visual state so we can start showing the result before all of it has fully streamed in. This protocol is a richer form that can *also* be converted to an HTML stream in order to speed up the initial, non-interactive render.

What about debugging issues with the react components in development? (as the component processed in server side and response will be special format) will developers have any clue on where to debug and find cause?

---

### @Dustin4444 — COMMENTED — 2025-10-18 15:36

#270

---
