import axios from 'axios'

const BASE_URL = 'http://localhost:8000/'

export const AxiosPanelistaChatbot = axios.create({
  baseURL: BASE_URL,
})
