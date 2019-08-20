import React from 'react';
import { API_ROOT } from '../../api-config';
import { withRouter } from 'react-router-dom';
import HighlightContainer from '../highlight/HighlightContainer';
import { Highlight } from '../highlight/Highlight';
import Model from '../Model'
import { truncateText } from '../DemoInput'
import ReactCountryFlag from "react-country-flag";

const apiUrl = () => `${API_ROOT}/predict/language_detection`

const title = "Language Detection";

const country={"fr":"French","es":"Spanish","gb":"English","pt":"Portugese","it":"Italian","de":"Deutch","ru":"Russian"}


const description = (
  <span>
  </span>
)

const descriptionEllipsed = undefined

const fields = [
    {name: "text", type: "TEXT"}
]


const Output = ({ responseData }) => {
 let{result}=responseData
 if(result=='en'){
 	result='gb'
 }
 let lang=country[result]
  return(       <div className="model__content model__content--ner-output">
					<div className="form__field"> 
						<h1>{lang}</h1>
 							<ReactCountryFlag  styleProps={{width: '300px',height: '200px',border: '1px solid black',backgroundSize: "cover"}} code={result} svg/>
 					</div>
 				</div>)
}



const examples = [
  ].map(sentence => ({sentence, snippet: truncateText(sentence)}))



const modelProps = {apiUrl, title, description, descriptionEllipsed,examples, fields, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)