
import React, { Component } from 'react';
import Calendar from 'react-calendar';
 
class Datepicker extends Component {

  
 
  render() {
    return (
      <div>
      <h3>{this.props.alert}</h3>
        <Calendar
          onChange={this.props.onChange}
          value={this.props.value}
        />
        <input type="text" value={this.props.realValue} onChange={this.props.onChange} />
      </div>
    );
  }
}

export default Datepicker