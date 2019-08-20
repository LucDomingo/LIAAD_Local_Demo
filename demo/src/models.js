import pampo from './components/demos/pampo'
import conta from './components/demos/conta_me_historias'
import yake from './components/demos/yake'
import sentiment_analyser from './components/demos/sentiment_analyser'
import text_generator from './components/demos/text_generator'
import title_suggestion from './components/demos/title_suggestion'
import sentence_classifier from './components/demos/sentence_classifier'
import summarize from './components/demos/summarize'
import presentation from './components/demos/presentation'
import test from './components/demos/test'
import language_detection from './components/demos/language_detection'
// This is the order in which they will appear in the menu
const modelGroups = [
    {
        label: "Named Entity Recognition",
        models: [
            {model: "PAMPO", name: "PAMPO", component: pampo},

        ]
    },
    {
        label: "Temporal Summarization",
        models: [
            {model: "Conta-me Historias", name: "Conta-me Historias", component: conta}
        ]
    },
    {
        label: "Keywords Extractor",
        models: [
            {model: "YAKE!", name: "YAKE!", component: yake}
        ]
    },
    {
        label: "NLP-Microservices",
        models: [
            {model: "text_generator", name: "Text generator", component: text_generator},
            {model: "title_suggestion", name: "Title suggestion", component: title_suggestion},
            {model: "summarize", name: "Summarize", component: summarize },
            {model: "sentence_classifier", name: "Sentence Classifier", component: sentence_classifier }

        ]
    }
]

// Create mapping model => component
let modelComponents = {}
modelGroups.forEach((mg) => mg.models.forEach(({model, component}) => modelComponents[model] = component));

export { modelComponents, modelGroups }
