import Koa from 'koa';
import Router from '@koa/router';
import bodyParser from 'koa-bodyparser';

const app = new Koa();
const router = new Router();

const users = [
  { id: 1, name: 'user1' },
  { id: 2, name: 'user2' },
];

let ip = [{ id: 0, ip: '121212' }];

router.get('/api/users', (ctx) => {
  ctx.body = {
    ok: true,
    users: users,
  };
});

router.get('/', (ctx) => {
  ctx.body = 'body';
});

router.post('/api/ip', (ctx) => {
  console.log(ctx.request.body);
  const lastId = ip[ip.length - 1].id;
  let newIp = {
    id: lastId + 1,
    ip: ctx.request.body.myIP,
  };
  ip.push(newIp);
  ctx.response.status = 201;
  ctx.body = {
    status: 'success',
    message: `등록완료`,
    result: ip,
  };
});

router.get('/api/ip', (ctx) => {
  ctx.body = ip;
});

app.use(bodyParser()); // 있어야 request body 해석 가능
app.use(router.routes()).use(router.allowedMethods());

app.listen(3000, () => console.log('Hi'));
