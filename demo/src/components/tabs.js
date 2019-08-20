import React, { Component } from 'react';
import { render } from 'react-dom';
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import ScrollableInkTabBar from 'rc-tabs/lib/ScrollableInkTabBar';
import 'rc-tabs/dist/rc-tabs.css'
import Datepicker from './Calendar'

class ControlledTabs extends React.Component {
  constructor(props) {
    super(props)
    this.choose="bonjour"
    this.list=[]
    this.value=undefined
    this.handleChange = e => {

    }
  }




  render() {
    var callback = function(key){}
    return (
    
    <Tabs
      defaultActiveKey="2"
      onChange={callback}
      renderTabBar={()=><ScrollableInkTabBar />}
      renderTabContent={()=><TabContent />}
    >
      <TabPane tab='tab 1' key="1"><Datepicker alert={this.choose}  realValue={this.list} value={this.value} onChange={this.handleChange} /></TabPane>
      <TabPane tab='tab 2' key="2">second</TabPane>
      <TabPane tab='tab 3' key="3">third</TabPane>
    </Tabs>
    );
  }
}



export default ControlledTabs