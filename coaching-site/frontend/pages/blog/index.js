import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import BackToTop from '../../components/BackToTop';
import { useLanguage } from '../../contexts/LanguageContext';

// Static blog posts data
const staticPosts = [
  {
    slug: 'mastering-stage-presence',
    title: 'Mastering Stage Presence: 5 Key Techniques',
    excerpt: 'Learn the essential techniques that will transform your stage presence and captivate any audience.',
    date: '2024-01-15',
    tags: ['stage-presence', 'public-speaking', 'confidence'],
    featured_image: '/pictures/blog/stage-presence.jpg'
  },
  {
    slug: 'voice-training-fundamentals',
    title: 'Voice Training Fundamentals for Speakers',
    excerpt: 'Discover the foundation of effective voice training and how to develop a powerful speaking voice.',
    date: '2024-01-10',
    tags: ['voice-training', 'communication', 'technique'],
    featured_image: '/pictures/blog/voice-training.jpg'
  },
  {
    slug: 'overcoming-public-speaking-anxiety',
    title: 'Overcoming Public Speaking Anxiety',
    excerpt: 'Practical strategies to conquer your fears and speak with confidence in any situation.',
    date: '2024-01-05',
    tags: ['anxiety', 'confidence', 'mindset'],
    featured_image: '/pictures/blog/anxiety.jpg'
  }
];

export default function Blog() {
  const { t } = useLanguage();
  const [filter, setFilter] = useState('');
  const [selectedTag, setSelectedTag] = useState('');

  // Get all unique tags from posts
  const allTags = [...new Set(staticPosts.flatMap(post => post.tags))];

  // Filter posts by search term and/or tag
  const filteredPosts = staticPosts.filter(post => {
    const matchesSearch = filter === '' || 
      post.title.toLowerCase().includes(filter.toLowerCase()) ||
      post.excerpt.toLowerCase().includes(filter.toLowerCase());
    
    const matchesTag = selectedTag === '' || post.tags.includes(selectedTag);
    
    return matchesSearch && matchesTag;
  });

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('blog.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('blog.description')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 py-20 md:py-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                <span className="bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                  {t('blog.hero.title')}
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-10 text-blue-100 max-w-3xl mx-auto leading-relaxed font-medium animate-fade-in-up delay-100">
                {t('blog.hero.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* Blog Posts Section */}
        <section className="py-16 md:py-24 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800 relative overflow-hidden">

          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              {/* Search and Filter */}
              <div className="mb-12">
                <div className="flex flex-col md:flex-row gap-4 md:items-center justify-between">
                  {/* Search */}
                  <div className="w-full md:w-1/2">
                    <label htmlFor="search" className="sr-only">{t('blog.search')}</label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg className="h-5 w-5 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                      </div>
                      <input
                        id="search"
                        type="search"
                        className="block w-full pl-10 pr-3 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                        placeholder={t('blog.searchPlaceholder')}
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                      />
                    </div>
                  </div>
                  
                  {/* Tags Filter */}
                  <div className="w-full md:w-1/2">
                    <label htmlFor="tag-filter" className="sr-only">{t('blog.filterByTag')}</label>
                    <select
                      id="tag-filter"
                      className="block w-full pl-3 pr-10 py-3 bg-white/10 border border-white/30 rounded-xl text-white backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                      value={selectedTag}
                      onChange={(e) => setSelectedTag(e.target.value)}
                    >
                      <option value="">{t('blog.allTags')}</option>
                      {allTags.map(tag => (
                        <option key={tag} value={tag}>{tag}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
              
              {/* Posts Grid */}
              {filteredPosts.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {filteredPosts.map((post) => (
                    <div key={post.slug} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-3xl overflow-hidden shadow-2xl transition duration-300 hover:shadow-3xl transform hover:scale-105 hover:rotate-1">
                      <Link href={`/blog/${post.slug}`} className="block">
                        {/* Featured image or placeholder */}
                        <div className="h-48 overflow-hidden">
                          {post.featured_image ? (
                            <img 
                              src={post.featured_image} 
                              alt={post.title}
                              className="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                            />
                          ) : (
                            <div className="w-full h-full bg-gradient-to-br from-indigo-400/20 to-purple-400/20 flex items-center justify-center">
                              <svg className="w-12 h-12 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                            </div>
                          )}
                        </div>
                        
                        <div className="p-6">
                          <div className="flex items-center mb-2">
                            <span className="text-sm text-blue-200">{post.date}</span>
                            {post.tags.length > 0 && (
                              <span className="mx-2 text-white/30">•</span>
                            )}
                            <div className="flex flex-wrap gap-2">
                              {post.tags.map(tag => (
                                <span 
                                  key={tag} 
                                  className="text-xs bg-yellow-400/20 text-yellow-200 px-2 py-1 rounded-full border border-yellow-400/30"
                                  onClick={(e) => {
                                    e.preventDefault();
                                    setSelectedTag(tag);
                                  }}
                                >
                                  {tag}
                                </span>
                              ))}
                            </div>
                          </div>
                          <h2 className="text-xl font-black mb-2 text-white drop-shadow-lg">{post.title}</h2>
                          <p className="text-white/90 mb-4 leading-relaxed">{post.excerpt}</p>
                          <span className="text-yellow-400 font-semibold">{t('blog.readMore')} →</span>
                        </div>
                      </Link>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl max-w-md mx-auto">
                    <svg className="w-16 h-16 text-white/60 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 className="text-xl font-black text-white mb-2 drop-shadow-lg">{t('blog.noPostsFound')}</h3>
                    <p className="text-white/80 mb-4">{t('blog.tryDifferentSearch')}</p>
                    <button 
                      className="inline-flex items-center justify-center px-6 py-3 text-sm font-semibold text-slate-900 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
                      onClick={() => {
                        setFilter('');
                        setSelectedTag('');
                      }}
                    >
                      {t('blog.clearFilters')}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>

      <Footer />
      <BackToTop />
    </div>
  );
}

