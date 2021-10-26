import Vue from "vue";
import axios from "axios"
import VueRouter, { RouteConfig } from "vue-router";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [      
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/home',
    name: 'adminHome',
    component: () => import('@/views/Admin.vue'),
    meta: '系统管理员首页',
    children: [
      {
        path: '/admin/queryhp',
        name: 'queryHp',
        component: () => import('@/views/admin/QueryHp.vue'),
        meta: '查询宿管信息'
      },
      {
        path: '/admin/querystu',
        name: 'queryStu',
        component: () => import('@/views/admin/QueryStu.vue'),
        meta: '查询学生信息'
      },
      {
        path: '/admin/managehp',
        name: 'manageHp',
        component: () => import('@/views/admin/ManageHp.vue'),
        meta: '管理宿管信息'
      },
      {
        path: '/admin/managestu',
        name: 'manageStu',
        component: () => import('@/views/admin/ManageStu.vue'),
        meta: '管理学生信息'
      }
    ]
  },
  {
    path: '/hphome',
    name: 'hpHome',
    component: () => import('@/views/Houseparent.vue'),
    meta: '宿管首页',
    children: [
      {
        path: '/hp/queryself',
        name: 'hpQuerySelf',
        component: () => import('@/views/hp/query/HpQuerySelf.vue'),
        meta: '查询个人信息'
      },
      {
        path: '/hp/querystu',
        name: 'hpQueryStu',
        component: () => import('@/views/hp/query/HpQueryStu.vue'),
        meta: '查询学生信息'
      },
      {
        path: '/hp/querynews',
        name: 'hpQueryNews',
        component: () => import('@/views/hp/query/HpQueryNews.vue'),
        meta: '查看公告'
      },  
      {
        path: '/hp/manageout',
        name: 'manageOut',
        component: () => import('@/views/hp/manage/ManageLeave.vue'),
        meta: '处理离校申请'
      },
      {
        path: '/hp/managerepairs',
        name: 'manageRepairs',
        component: () => import('@/views/hp/manage/ManageRepairs.vue'),
        meta: '处理报修申请'
      },
      {
        path: '/hp/postnews',
        name: 'postNews',
        component: () => import('@/views/hp/manage/PostNews.vue'),
        meta: '发布公告'
      }
    ]
  },
  {
    path: '/headhphome',
    name: 'headHpHome',
    component: () => import('@/views/headHp.vue'),
    meta: '总宿管首页',
    children: [
      {
        path: '/headhp/headqueryhp',
        name: 'headQueryHp',
        component: () => import('@/views/headhp/query/headQueryHp.vue'),
        meta: '查询宿管信息'
      },
      {
        path: '/headhp/querystu',
        name: 'headHpQueryStu',
        component: () => import('@/views/headhp/query/HpQueryStu.vue'),
        meta: '查询学生信息'
      },
      {
        path: '/headhp/querynews',
        name: 'headHpQueryStu',
        component: () => import('@/views/headhp/query/HpQueryNews.vue'),
        meta: '查看公告'
      },  
      {
        path: '/headhp/managein',
        name: 'headHpManageCheckin',
        component: () => import('@/views/headhp/manage/ManageCheckIn.vue'),
        meta: '处理入住申请'
      },
      {
        path: '/headhp/manageout',
        name: 'headHpManageLeave',
        component: () => import('@/views/headhp/manage/ManageLeave.vue'),
        meta: '处理离校申请'
      },
      {
        path: '/headhp/managerepairs',
        name: 'headHpManageRepairs',
        component: () => import('@/views/headhp/manage/ManageRepairs.vue'),
        meta: '处理报修申请'
      },
      {
        path: '/headhp/postnews',
        name: 'headHpPostNews',
        component: () => import('@/views/headhp/manage/PostNews.vue'),
        meta: '发布公告'
      }
    ]
  },
  {
    path: '/stuhome',
    name: 'stuHome',
    component: () => import('@/views/Student.vue'),
    meta: '学生首页',
    children: [
      {
        path: '/stu/query',
        name: 'queryHp',
        component: () => import('@/views/stu/StuQuarySelfInfo.vue'),
        meta: '查询信息'
      },
      {
        path: '/stu/applyin',
        name: 'queryStu',
        component: () => import('@/views/stu/Applyin.vue'),
        meta: '申请入住'
      },
      {
        path: '/stu/applyleave',
        name: 'manageHp',
        component: () => import('@/views/stu/leaveApply.vue'),
        meta: '申请离校'
      },
      {
        path: '/stu/payfee',
        name: 'manageStu',
        component: () => import('@/views/stu/Payfee.vue'),
        meta: '水电缴费'
      },
      {
        path: '/stu/applyrepairs',
        name: 'manageStu',
        component: () => import('@/views/stu/Applyrepairs.vue'),
        meta: '公物报修'
      },
      {
        path: '/stu/querynews',
        name: 'stuQueryNews',
        component: () => import('@/views/stu//StuQueryNews.vue'),
        meta: '查看公告'
      }
    ]
  },
  {
    path: '/error',
    name: 'error',
    component: () => import('@/views/Error.vue')
  },
  {
    path: '*',
    redirect: '/error'
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;

// router.beforeEach((to, from, next) => {
//   if(to.name!=='Login'||to.path!=='/')
//   {
//   axios({
//     method: "get",
//     url: "http://localhost:8080/api/user/get_usertype",
//   }).then((res) => {
    
//     if(to.path!=='/login'&&res.status!==200)
//     next({name:'error'})
//     else next()
//   })
//   }
// });