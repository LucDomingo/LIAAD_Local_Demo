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

const apiUrl = () => `${API_ROOT}/predict/classify`

const title = "Sentence Classifier";


const description = (
  <span>
    <span>
       
    </span>
  </span>
)

const descriptionEllipsed = undefined

const fields = [
    {name: "text", type: "TABS2", input:"opt_sen"}
]
const TokenSpan = ({ text,entity,prob}) => {
    // Lookup table for entity style values:
    const entityLookup = {
      "background": {
        tooltip: "Person",
        color: "fuchsia"
      },
      "unassigned": {
        tooltip: "Location",
        color: "green"
      },
      "objective": {
        tooltip: "Organization",
        color: "blue"
      },
      "methods": {
        tooltip: "Miscellaneous",
        color: "gray"
      },
      "results": {
        tooltip: "Person",
        color: "pink"
      },
      "conclusions": {
        tooltip: "Cardinal Number",
        color: "orange"
      },
      "EVENT": {
        tooltip: "Event",
        color: "green"
      },
      "DATE": {
        tooltip: "Date",
        color: "fuchsia"
      },
      "FAC": {
        tooltip: "Facility",
        color: "cobalt"
      },
      "GPE": {
        tooltip: "Country/City/State",
        color: "teal"
      },
      "LANGUAGE": {
        tooltip: "Language",
        color: "red"
      },
      "LAW": {
        tooltip: "Law",
        color: "brown"
      },
      // LOC - see above
      "MONEY": {
        tooltip: "Monetary Value",
        color: "orange"
      },
      "NORP": {
        tooltip: "Nationalities, Religious/Political Groups",
        color: "green"
      },
      "ORDINAL": {
        tooltip: "Ordinal Value",
        color: "orange"
      },
      // ORG - see above.
      "PERCENT": {
        tooltip: "Percentage",
        color: "orange"
      },
      "PRODUCT": {
        tooltip: "Product",
        color: "purple"
      },
      "QUANTITY": {
        tooltip: "Quantity",
        color: "orange"
      },
      "TIME": {
        tooltip: "Time",
        color: "fuchsia"
      },
      "WORK_OF_ART": {
        tooltip: "Work of Art/Media",
        color: "tan"
      },
    }

    if (entity !== null) { // If token has entity value:
      // Display entity text wrapped in a <Highlight /> component.
      return (<Highlight label={entity} color={entityLookup[entity].color} tooltip={prob}>{text} </Highlight>);
    }
}

const Output = ({ responseData }) => {
 
    const {result}=responseData


    return (

      <div className="model__content model__content--ner-output">
        <div className="form__field">
          <HighlightContainer layout="bottom-labels">
            {result.map((token, i) => <TokenSpan entity={token[0]} text={token[1]} prob={token[2]} />)}
          </HighlightContainer>
        </div>
      </div>

    )
}




const examples = [
  ].map(sentence => ({sentence, snippet: truncateText(sentence)}))



const modelProps = {apiUrl, title, description, descriptionEllipsed,examples, fields, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)