'use client'

import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const API_URL = 'http://localhost:8000'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

interface QuizQuestion {
  question: string
  options: string[]
  correct_answer: string
  explanation: string
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'chat' | 'quiz' | 'topics'>('chat')
  const [topics, setTopics] = useState<any>(null)
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([])
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0)
  const [quizScore, setQuizScore] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [showExplanation, setShowExplanation] = useState(false)
  const [stats, setStats] = useState<any>(null)

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Load topics and stats on mount
    loadTopics()
    loadStats()
  }, [])

  const loadTopics = async () => {
    try {
      const response = await axios.get(`${API_URL}/topics`)
      setTopics(response.data)
    } catch (error) {
      console.error('Error loading topics:', error)
    }
  }

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats`)
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        question: input,
        conversation_history: messages
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const generateQuiz = async (topic: string, difficulty: string = 'medium') => {
    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/quiz`, {
        topic,
        difficulty,
        num_questions: 5
      })

      setQuizQuestions(response.data.questions)
      setCurrentQuizIndex(0)
      setQuizScore(0)
      setSelectedAnswer(null)
      setShowExplanation(false)
      setActiveTab('quiz')
    } catch (error) {
      console.error('Error generating quiz:', error)
      alert('Error generating quiz. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleQuizAnswer = (answer: string) => {
    setSelectedAnswer(answer)
    setShowExplanation(true)

    if (answer === quizQuestions[currentQuizIndex].correct_answer) {
      setQuizScore(prev => prev + 1)
    }
  }

  const nextQuestion = () => {
    if (currentQuizIndex < quizQuestions.length - 1) {
      setCurrentQuizIndex(prev => prev + 1)
      setSelectedAnswer(null)
      setShowExplanation(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-aws-blue text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">AWS AI Learning Platform</h1>
              <p className="text-gray-300 mt-1">Master AI/ML Services with RAG-Powered Learning</p>
            </div>
            {stats && (
              <div className="bg-aws-orange/20 rounded-lg px-4 py-2">
                <div className="text-sm text-gray-300">Knowledge Base</div>
                <div className="text-2xl font-bold">{stats.total_documents} docs</div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-1">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === 'chat'
                  ? 'border-b-2 border-aws-orange text-aws-orange'
                  : 'text-gray-600 hover:text-aws-orange'
              }`}
            >
              💬 AI Tutor
            </button>
            <button
              onClick={() => setActiveTab('quiz')}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === 'quiz'
                  ? 'border-b-2 border-aws-orange text-aws-orange'
                  : 'text-gray-600 hover:text-aws-orange'
              }`}
            >
              📝 Practice Quizzes
            </button>
            <button
              onClick={() => setActiveTab('topics')}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === 'topics'
                  ? 'border-b-2 border-aws-orange text-aws-orange'
                  : 'text-gray-600 hover:text-aws-orange'
              }`}
            >
              📚 Topics
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="bg-white rounded-lg shadow-lg h-[calc(100vh-280px)] flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.length === 0 && (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🤖</div>
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">
                    Welcome to Your AI Tutor!
                  </h3>
                  <p className="text-gray-500 mb-6">
                    Ask me anything about AWS AI/ML services, certifications, or best practices.
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                    {[
                      'What is Amazon SageMaker?',
                      'Explain Amazon Bedrock and its use cases',
                      'How do I prepare for AI Practitioner exam?',
                      'Compare Comprehend vs Rekognition for text'
                    ].map((q, i) => (
                      <button
                        key={i}
                        onClick={() => setInput(q)}
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-aws-orange hover:bg-orange-50 transition-colors text-left"
                      >
                        <div className="text-sm text-gray-600">{q}</div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-animation flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-3xl rounded-lg p-4 ${
                      message.role === 'user'
                        ? 'bg-aws-orange text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-300">
                        <div className="text-xs font-semibold mb-1">Sources:</div>
                        {message.sources.map((source, i) => (
                          <div key={i} className="text-xs opacity-75">
                            📄 {source}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg p-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 p-4">
              <div className="flex space-x-4">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about AWS AI/ML services..."
                  className="flex-1 border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-aws-orange"
                  disabled={loading}
                />
                <button
                  onClick={sendMessage}
                  disabled={loading || !input.trim()}
                  className="bg-aws-orange text-white px-8 py-3 rounded-lg font-medium hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Quiz Tab */}
        {activeTab === 'quiz' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            {quizQuestions.length === 0 ? (
              <div>
                <h2 className="text-2xl font-bold mb-6">Practice Quizzes</h2>
                <p className="text-gray-600 mb-6">
                  Test your knowledge with AI-generated quizzes on AWS AI/ML topics
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {topics?.ai_services?.map((service: string, i: number) => (
                    <button
                      key={i}
                      onClick={() => generateQuiz(service)}
                      className="p-6 border-2 border-gray-200 rounded-lg hover:border-aws-orange hover:bg-orange-50 transition-colors text-left"
                    >
                      <div className="text-lg font-semibold mb-2">{service}</div>
                      <div className="text-sm text-gray-600">5 Questions • Medium</div>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div>
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-2xl font-bold">
                      Question {currentQuizIndex + 1} of {quizQuestions.length}
                    </h2>
                    <div className="text-lg font-semibold text-aws-orange">
                      Score: {quizScore}/{quizQuestions.length}
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-aws-orange h-2 rounded-full transition-all"
                      style={{
                        width: `${((currentQuizIndex + 1) / quizQuestions.length) * 100}%`
                      }}
                    ></div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-xl mb-6">{quizQuestions[currentQuizIndex].question}</h3>
                  <div className="space-y-3">
                    {quizQuestions[currentQuizIndex].options.map((option, i) => {
                      const letter = option.charAt(0)
                      const isCorrect = letter === quizQuestions[currentQuizIndex].correct_answer
                      const isSelected = letter === selectedAnswer

                      return (
                        <button
                          key={i}
                          onClick={() => !selectedAnswer && handleQuizAnswer(letter)}
                          disabled={selectedAnswer !== null}
                          className={`w-full p-4 rounded-lg border-2 text-left transition-all ${
                            !selectedAnswer
                              ? 'border-gray-300 hover:border-aws-orange hover:bg-orange-50'
                              : isSelected && isCorrect
                              ? 'border-green-500 bg-green-50'
                              : isSelected && !isCorrect
                              ? 'border-red-500 bg-red-50'
                              : isCorrect && selectedAnswer
                              ? 'border-green-500 bg-green-50'
                              : 'border-gray-300'
                          }`}
                        >
                          {option}
                        </button>
                      )
                    })}
                  </div>
                </div>

                {showExplanation && (
                  <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-6">
                    <div className="font-semibold mb-2">Explanation:</div>
                    <div className="text-gray-700">
                      {quizQuestions[currentQuizIndex].explanation}
                    </div>
                  </div>
                )}

                <div className="flex justify-between">
                  <button
                    onClick={() => {
                      setQuizQuestions([])
                      setCurrentQuizIndex(0)
                      setQuizScore(0)
                    }}
                    className="px-6 py-3 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Exit Quiz
                  </button>
                  {showExplanation && currentQuizIndex < quizQuestions.length - 1 && (
                    <button
                      onClick={nextQuestion}
                      className="px-6 py-3 bg-aws-orange text-white rounded-lg hover:bg-orange-600 transition-colors"
                    >
                      Next Question →
                    </button>
                  )}
                  {showExplanation && currentQuizIndex === quizQuestions.length - 1 && (
                    <div className="text-right">
                      <div className="text-xl font-bold text-aws-orange mb-2">
                        Quiz Complete!
                      </div>
                      <div className="text-gray-600">
                        Final Score: {quizScore}/{quizQuestions.length} (
                        {Math.round((quizScore / quizQuestions.length) * 100)}%)
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Topics Tab */}
        {activeTab === 'topics' && topics && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-6">AWS AI/ML Topics</h2>

            <div className="mb-8">
              <h3 className="text-xl font-semibold mb-4 text-aws-orange">🤖 AI Services</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {topics.ai_services.map((service: string, i: number) => (
                  <div
                    key={i}
                    onClick={() => {
                      setInput(`Tell me about ${service}`)
                      setActiveTab('chat')
                    }}
                    className="p-3 border-2 border-gray-200 rounded-lg hover:border-aws-orange hover:bg-orange-50 cursor-pointer transition-colors"
                  >
                    {service}
                  </div>
                ))}
              </div>
            </div>

            <div className="mb-8">
              <h3 className="text-xl font-semibold mb-4 text-aws-orange">⚙️ ML Infrastructure</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {topics.ml_infrastructure.map((service: string, i: number) => (
                  <div
                    key={i}
                    onClick={() => {
                      setInput(`Tell me about ${service}`)
                      setActiveTab('chat')
                    }}
                    className="p-3 border-2 border-gray-200 rounded-lg hover:border-aws-orange hover:bg-orange-50 cursor-pointer transition-colors"
                  >
                    {service}
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-4 text-aws-orange">🎓 Certifications</h3>
              <div className="space-y-3">
                {topics.certifications.map((cert: string, i: number) => (
                  <div
                    key={i}
                    className="p-4 border-2 border-gray-200 rounded-lg hover:border-aws-orange hover:bg-orange-50 cursor-pointer transition-colors"
                  >
                    <div className="font-semibold">{cert}</div>
                    <button
                      onClick={() => generateQuiz(cert, 'medium')}
                      className="mt-2 px-4 py-2 bg-aws-orange text-white rounded text-sm hover:bg-orange-600 transition-colors"
                    >
                      Generate Practice Quiz
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
