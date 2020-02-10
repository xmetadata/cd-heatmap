import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/blockset',
    method: 'get',
    params
  })
}

export function getDetail(uuid) {
  return request({
    url: '/blockset/' + uuid,
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/blockset',
    method: 'post',
    data
  })
}

export function update(uuid, data) {
  return request({
    url: '/blockset/' + uuid,
    method: 'put',
    data
  })
}

export function remove(uuid) {
  return request({
    url: '/blockset/' + uuid,
    method: 'delete'
  })
}
