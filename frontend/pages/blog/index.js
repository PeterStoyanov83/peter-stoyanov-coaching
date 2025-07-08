import { useState } from 'react';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../../components/Header';
import Footer from '../../components/Footer';

export default function Blog({ posts }) {
  const { t } = useTranslation('common');
  const [filter, setFilter] = useState('');
  const [selectedTag, setSelectedTag] = useState('');

  // Get all unique tags from posts
  const allTags = [...new Set(posts.flatMap(post => post.tags))];

  // Filter posts by search term and/or tag
  const filteredPosts = posts.filter(post => {
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
        <section className="relative bg-gray-50 py-20 md:py-32">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                {t('blog.hero.title')}
              </h1>
              <p className="text-xl md:text-2xl mb-10 text-gray-600">
                {t('blog.hero.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* Blog Posts Section */}
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              {/* Search and Filter */}
              <div className="mb-12">
                <div className="flex flex-col md:flex-row gap-4 md:items-center justify-between">
                  {/* Search */}
                  <div className="w-full md:w-1/2">
                    <label htmlFor="search" className="sr-only">{t('blog.search')}</label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                      </div>
                      <input
                        id="search"
                        type="search"
                        className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
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
                      className="block w-full pl-3 pr-10 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
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
                    <div key={post.slug} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-md transition duration-300 hover:shadow-lg">
                      <Link href={`/blog/${post.slug}`} className="block">
                        {/* If you have featured images, add them here */}
                        <div className="h-48 bg-gray-200"></div>
                        
                        <div className="p-6">
                          <div className="flex items-center mb-2">
                            <span className="text-sm text-gray-500">{post.date}</span>
                            {post.tags.length > 0 && (
                              <span className="mx-2 text-gray-300">•</span>
                            )}
                            <div className="flex flex-wrap gap-2">
                              {post.tags.map(tag => (
                                <span 
                                  key={tag} 
                                  className="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full"
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
                          <h2 className="text-xl font-semibold mb-2 text-gray-900">{post.title}</h2>
                          <p className="text-gray-600 mb-4">{post.excerpt}</p>
                          <span className="text-indigo-600 font-medium">{t('blog.readMore')} →</span>
                        </div>
                      </Link>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">{t('blog.noPostsFound')}</h3>
                  <p className="text-gray-500">{t('blog.tryDifferentSearch')}</p>
                  <button 
                    className="mt-4 text-indigo-600 font-medium"
                    onClick={() => {
                      setFilter('');
                      setSelectedTag('');
                    }}
                  >
                    {t('blog.clearFilters')}
                  </button>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export async function getStaticProps({ locale }) {
  // In a real app, you would fetch this from your API
  // For now, we'll use dummy data
  const posts = [
    {
      slug: 'mastering-public-speaking',
      title: 'Mastering Public Speaking: 5 Theater Techniques That Work',
      content: '...',
      excerpt: 'Learn how theater techniques can transform your public speaking skills and help you connect with any audience.',
      date: '2023-05-15',
      tags: ['public-speaking', 'theater']
    },
    {
      slug: 'voice-projection-tips',
      title: 'Voice Projection Tips for Effective Communication',
      content: '...',
      excerpt: 'Discover how to use your voice effectively to command attention and convey your message with impact.',
      date: '2023-04-22',
      tags: ['voice', 'communication']
    },
    {
      slug: 'body-language-secrets',
      title: 'Body Language Secrets from Professional Actors',
      content: '...',
      excerpt: 'Explore how professional actors use body language to enhance their performances and how you can apply these techniques.',
      date: '2023-03-10',
      tags: ['body-language', 'acting']
    },
    {
      slug: 'overcoming-stage-fright',
      title: 'Overcoming Stage Fright: A Step-by-Step Guide',
      content: '...',
      excerpt: 'Learn practical techniques to manage anxiety and perform confidently in front of any audience.',
      date: '2023-02-18',
      tags: ['anxiety', 'performance']
    },
    {
      slug: 'storytelling-for-business',
      title: 'Storytelling for Business: Engage Your Audience',
      content: '...',
      excerpt: 'Discover how to use storytelling techniques to make your business presentations more engaging and memorable.',
      date: '2023-01-25',
      tags: ['storytelling', 'business']
    },
    {
      slug: 'breathing-techniques',
      title: 'Breathing Techniques for Better Speech and Presence',
      content: '...',
      excerpt: 'Master the art of breathing to improve your vocal quality, reduce stress, and enhance your overall presence.',
      date: '2022-12-12',
      tags: ['breathing', 'voice']
    }
  ];

  return {
    props: {
      ...(await serverSideTranslations(locale, ['common'])),
      posts
    },
  };
}