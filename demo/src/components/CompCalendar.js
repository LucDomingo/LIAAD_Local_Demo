import React, { Component } from 'react'
import Calendar from './Calendar'

class ComponentUsingCalendar extends Component {
  constructor(props) {
    super(props)
    const date = new Date()
    const startDate = date.getTime()
    this.DEFAULT_START_DATE = startDate, // Today
    this.DEFAULT_END_DATE = new Date(startDate).setDate(date.getDate() + 6) // Today + 6 days
  }

  render = () => (
    <Calendar
      startDate={this.DEFAULT_START_DATE}
      endDate={this.DEFAULT_END_DATE}
    />
  )
}

export default ComponentUsingCalendar