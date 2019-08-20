import React from 'react';
import { API_ROOT } from '../../api-config';
import { withRouter } from 'react-router-dom';
import Model from '../Model'
import { truncateText } from '../DemoInput'


const title = "NLP Microservices";
const apiUrl = () => `${API_ROOT}`




const description = (
  <span>
  <h2>Algorithmic Science News (ASN) </h2>
    <span>
         Helping journalists to write science news.
        A platform that summarizes and clarifies a scientific paper, and suggests how to write a news article about it.
    </span>
     <br/>
    <a href = "http://asn.inesctec.pt/" target="_blank" rel="noopener noreferrer">
      {' '}See More{' '}</a>
  </span>
)

const fields = [
 {name: "", type: "PRESENTATION"}
]

const descriptionEllipsed = undefined

const Output = ({ responseData }) => {

}


const examples = [
  ].map(sentence => ({sentence, snippet: truncateText(sentence)}))



const modelProps = {apiUrl, title, description, descriptionEllipsed,examples, fields, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)