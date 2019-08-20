/* eslint-disable */
import React from 'react'
import TagsInput from 'react-tagsinput'
import 'react-tagsinput/react-tagsinput.css' // If using WebPack and style-loader.
import Autosuggest from 'react-autosuggest'
import AutosizeInput from 'react-input-autosize'
import {findDOMNode, render} from 'react-dom'
import SimpleExample from "./input_tags/components/simple";
import AutosizeExample from "./input_tags/components/autosize";
import AutocompleteExample from "./input_tags/components/autocomplete";
import EmailExample from "./input_tags/components/email";
import FormExample from "./input_tags/components/form";
import AutoaddExample from "./input_tags/components/autoadd";
import ValidationCallbackExample from "./input_tags/components/validationcallback";



class ListDomain extends React.Component {
  render () {
    return (
      <div>

        <AutocompleteExample />

      </div>
    )
  }
}

export default ListDomain
