import request from '@/utils/request'

export function login(data) {
  return request({
    // url: '/user/login',
    url: '/auth',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // url: '/user/info',
    url: '/userinfo',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    // url: '/user/logout',
    url: '/logout',
    method: 'post'
  })
}
