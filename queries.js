const { Pool, Client } = require('pg')
const connectionString = 'postgres://ancbfwymcoubkj:7d8442ce0898e328ce41a220edcb4a1d11bd64273d9c740119b7164d0095f757@ec2-34-230-231-71.compute-1.amazonaws.com:5432/damca7lp4ld4tb'
const pool = new Pool({
  connectionString: connectionString,
  ssl: {
  	rejectUnauthorized: false
  }
})
const getDate = (request, response) => {
  pool.query('SELECT date FROM covid19_scraping_data_table', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getNumberOfCases = (request, response) => {
  pool.query('SELECT cases FROM covid19_scraping_data_table', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getID = (request, response) => {
  pool.query('SELECT id FROM covid19_scraping_data_table', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getAll = (request, response) => {
  pool.query('SELECT * FROM covid19_scraping_data_table', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

module.exports = {
  getDate,
  getNumberOfCases,
  getID,
  getAll
}