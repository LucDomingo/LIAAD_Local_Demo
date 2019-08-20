import React from 'react';
import { API_ROOT } from '../../api-config';
import { withRouter } from 'react-router-dom';
import HighlightContainer from '../highlight/HighlightContainer';
import { Highlight } from '../highlight/Highlight';
import Model from '../Model'
import { truncateText } from '../DemoInput'
import Datepicker from '../Calendar'
import Timeline from 'react-time-line'


const apiUrl = () => `${API_ROOT}/predict/conta`

const title = "Conta me historias";



const description = (
  <span>
    <span>
    This package can retrive articles from Arquivo.pt web archive and produce a temporal summarization.
    </span>
    <br/>
    <a href = "http://contamehistorias.inesctec.pt/arquivopt/" target="_blank" rel="noopener noreferrer">
      {' '}Demo website{' '}
    </a>
    <br/>
    <a href = "https://github.com/LIAAD/TemporalSummarizationFramework" target="_blank" rel="noopener noreferrer">{' '} Github {' '}</a>
    <br/>
  </span>

)

const descriptionEllipsed = (
  <span>
    This package can retrive articles from Arquivo.pt web archive and produce a temporal summarization.
  </span>
)

const fields = [
    {name: "date", label: "Specify time frame to restrict your query", type: "CALENDAR",optional:true
    },
    {name: "domain",label: "Specify websites to restrict your query", type: "DOMAIN",optional:true
    },
    {name: "keywords", label: "Choose relevant keyphrases", type: "TEXT_AREA",
     placeholder: "Dilma Rousseff" }


]



const Output = ({ responseData }) => {
 
    const { text ,date,article} = responseData
    console.log(date)

    let txt=[]

    let time={'ts':'','text': ''}


    let tab=[]


   date.map(  (item,i)=> {                              
                                          article[i].map((it, i) => {time['text']=it;tab.push({'ts':item.substr(0,19),'text': time['text']}) }); 
                                          tab.push({'ts':item.substr(26,44),'text': undefined})
                                          
                                    


                          }      
            
  
  )
      
            let rtab=tab
            console.log(rtab)

     return(<Timeline items={rtab} />)
}

const examples =[]



const modelProps = {apiUrl, title, description, descriptionEllipsed, fields, examples, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)