import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/dataset',
    method: 'get',
    params
  })
}

export function getDetail(uuid) {
  return request({
    url: '/dataset/' + uuid,
    method: 'get'
  })
}

export function getData(uuid, data) {
  return request({
    url: '/dataset/' + uuid,
    method: 'post',
    data
  })
}

export function create(data) {
  return request({
    url: '/dataset',
    method: 'post',
    data
  })
}

export function update(uuid, data) {
  return request({
    url: '/dataset/' + uuid,
    method: 'put',
    data
  })
}

export function remove(uuid) {
  return request({
    url: '/dataset/' + uuid,
    method: 'delete'
  })
}
