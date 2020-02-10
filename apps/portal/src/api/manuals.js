import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/manuals',
    method: 'get',
    params
  })
}

export function getDetail(uuid) {
  return request({
    url: '/manuals/' + uuid,
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/manuals',
    method: 'post',
    data
  })
}

export function update(uuid, data) {
  return request({
    url: '/manuals/' + uuid,
    method: 'put',
    data
  })
}

export function remove(uuid) {
  return request({
    url: '/manuals/' + uuid,
    method: 'delete'
  })
}
