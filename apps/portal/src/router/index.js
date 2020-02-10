import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/blockset/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/heatmap',
    children: [{
      path: 'heatmap',
      name: 'Heatmap',
      component: () => import('@/views/heatmap/index'),
      meta: { title: '热力地图', icon: 'international' }
    }]
  },

  {
    path: '/dataset',
    component: Layout,
    redirect: '/dataset/list',
    name: 'Dataset',
    meta: {
      title: '数据管理',
      icon: 'excel'
    },
    children: [
      {
        path: 'create',
        component: () => import('@/views/dataset/create'),
        name: 'CreateDataset',
        meta: { title: '创建数据', activeMenu: '/dataset/list' },
        hidden: true
      },
      {
        path: 'edit/:uuid',
        component: () => import('@/views/dataset/edit'),
        name: 'EditDataset',
        meta: { title: '编辑数据', noCache: true, activeMenu: '/dataset/list' },
        hidden: true
      },
      {
        path: 'list',
        component: () => import('@/views/dataset/list'),
        name: 'DatasetList',
        meta: { title: '数据列表', icon: 'list' },
        hidden: true
      }
    ]
  },

  {
    path: '/blockset',
    component: Layout,
    redirect: '/blockset/list',
    name: 'Blockset',
    meta: {
      title: '板块管理',
      icon: 'component'
    },
    children: [
      {
        path: 'create',
        component: () => import('@/views/blockset/create'),
        name: 'CreateBlockset',
        meta: { title: '创建板块', activeMenu: '/blockset/list' },
        hidden: true
      },
      {
        path: 'edit/:uuid',
        component: () => import('@/views/blockset/edit'),
        name: 'EditBlockset',
        meta: { title: '编辑板块', noCache: true, activeMenu: '/blockset/list' },
        hidden: true
      },
      {
        path: 'list',
        component: () => import('@/views/blockset/list'),
        name: 'BlocksetList',
        meta: { title: '板块列表', icon: 'list' },
        hidden: true
      },
      {
        path: 'preview/:uuid',
        component: () => import('@/views/blockset/preview'),
        name: 'EditBlockset',
        meta: { title: '板块预览', noCache: true, activeMenu: '/blockset/list' },
        hidden: true
      }
    ]
  },

  {
    path: '/manuals',
    component: Layout,
    redirect: '/manuals',
    children: [{
      path: 'manuals',
      name: 'Manuals',
      component: () => import('@/views/manuals/index'),
      meta: { title: '用户手册', icon: 'education' }
    }]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
