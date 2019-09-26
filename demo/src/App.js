import React from 'react';
import { API_ROOT } from './api-config';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';
import Menu from './components/Menu';
import ModelIntro from './components/ModelIntro';
import { modelComponents } from './models'
import { PaneTop } from './components/Pane';
import WaitingForPermalink from './components/WaitingForPermalink';



import './css/App.css';
import './css/fonts.css';
import './css/icons.css';
import './css/form.css';
import './css/Accordion.css';
import './css/hierplane-overrides.css';
import './css/visualization-types.css';



const DEFAULT_PATH = "/PAMPO"
const App = () => (
  <Router>
    <div>
      <Route exact path="/" render={() => (
        <Redirect to={DEFAULT_PATH}/>
      )}/>
      <Route path="/:model/:slug?" component={Demo}/>
    </div>
  </Router>
)

class Demo extends React.Component {
  constructor(props) {
    super(props);

    const { model, slug } = props.match.params;

    this.state = {
      slug: slug,
      selectedModel: model,
      requestData: null,
      responseData: null,
      expandedModelGroupIndexes: [0, 1, 2, 3, 4] 
    };

    this.clearData = () => {
      this.setState({requestData: null, responseData: null})
    }
    this.handleExpandModelGroup = (expandedModelGroupIndexes) => {
      this.setState({ expandedModelGroupIndexes: expandedModelGroupIndexes });
    };
    props.history.listen((location, action) => {
      const { state } = location;
      if (state) {
        const { requestData, responseData } = state;
        this.setState({requestData, responseData})
      }
    });
  }

  componentWillReceiveProps({ match }) {
    const { model, slug } = match.params;
    this.setState({selectedModel: model, slug: slug});
  }
  componentDidMount() {
    const { slug, responseData } = this.state;

    if (slug && !responseData) {
      fetch(`${API_ROOT}/permadata`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"slug": slug})
      }).then(function(response) {
        return response.json();
      }).then((json) => {
        const { requestData, responseData } = json;
        this.setState({requestData, responseData});
      }).catch((error) => {
        this.setState({outputState: "error"});
        console.error(error);
      });
    }
  }

  render() {
    const { slug, selectedModel, requestData, responseData, expandedModelGroupIndexes } = this.state;

    const ModelComponent = () => {
      if (slug && !responseData) {
        return (<WaitingForPermalink/>)
      } else if (modelComponents[selectedModel]) {
          // This is a model we know the component for, so render it.
          return React.createElement(modelComponents[selectedModel], {requestData, responseData, selectedModel})
      } else if (selectedModel === "user-models") {
        const modelRequest = "User Contributed Models"
        const modelDescription = (
          <span>
            <span>
            </span>
             <span>
            </span>
          </span>
      );

        return (
          <div className="pane__horizontal model">
            <div className='model__content'>
              <PaneTop>
                <ModelIntro title={modelRequest} description={modelDescription}/>
              </PaneTop>
              </div>
          </div>

        )
      }
    }

    return (
      <div className="pane-container">
        <Menu
          selectedModel={selectedModel}
          expandedModelGroupIndexes={expandedModelGroupIndexes}
          clearData={this.clearData}
          onExpandModelGroup={this.handleExpandModelGroup}/>
        <ModelComponent />
      </div>
    );
  }
}

export default App;
