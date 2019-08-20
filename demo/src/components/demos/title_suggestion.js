import React from 'react';
import { API_ROOT } from '../../api-config';
import { withRouter } from 'react-router-dom';
import HighlightContainer from '../highlight/HighlightContainer';
import { Highlight } from '../highlight/Highlight';
import Model from '../Model'
import { truncateText } from '../DemoInput'
import WordCloud from 'react-d3-cloud';
import 'rc-tabs/dist/rc-tabs.css'
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import ScrollableInkTabBar from 'rc-tabs/lib/ScrollableInkTabBar';

const apiUrl = () => `${API_ROOT}/predict/title`

const title = "Title Suggestion";




const description = (
  <span>
    <span>
    </span>
  </span>
)

const descriptionEllipsed = undefined

const fields = [
    {name: "text", type: "TEXT"}
]



const Output = ({ responseData }) => {



    const {original,result}=responseData


    return (<div className="model__content model__content--ner-output">
          <div className="form__field"> 
            <h1>{result}</h1>
           <p>{original}</p></div></div>


    )
}


const examples = [
  ].map(sentence => ({sentence, snippet: truncateText(sentence)}))



const modelProps = {apiUrl, title, description, descriptionEllipsed,examples, fields, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)