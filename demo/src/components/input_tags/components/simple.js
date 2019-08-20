import React from 'react'

import TagsInput from 'react-tagsinput'

class SimpleExample extends React.Component {
  constructor () {
    super()
    this.state = {tags: []}

    this.handleChange = tags => {
    this.setState({tags})
  }
  }



  render () {
    return <TagsInput value={this.state.tags} onChange={this.handleChange} />
  }
}

export default SimpleExample
