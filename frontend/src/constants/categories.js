export const CATEGORY_TEXT_MAP = Object.freeze({
  '[0]': '井盖完好',
  '[1]': '井盖破损',
  '[2]': '井盖缺失',
  '[3]': '井盖未盖',
  '[4]': '井圈问题'
})

export const CATEGORY_TAG_TYPE_MAP = Object.freeze({
  '[0]': 'success',
  '[1]': 'warning',
  '[2]': 'danger',
  '[3]': 'danger',
  '[4]': 'warning'
})

export const getCategoryText = (categoryCode) => CATEGORY_TEXT_MAP[categoryCode] || '未分类'

export const getCategoryTagType = (categoryCode) => CATEGORY_TAG_TYPE_MAP[categoryCode] || 'info'
