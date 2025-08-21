import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';
import { blogPosts, blogTags } from '../data/blogPosts';

export default function Blog() {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTag, setSelectedTag] = useState('');

  const filteredPosts = blogPosts.filter(post => {
    const matchesSearch = post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         post.excerpt.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTag = selectedTag === '' || post.tags.includes(selectedTag);
    return matchesSearch && matchesTag;
  });

  return (
    <>
      <Head>
        <title>{t('blog.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('blog.description')} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white">
        <Header />
        
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-indigo-900 via-indigo-800 to-purple-800 text-white py-20 pt-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                {t('blog.hero.title')}
              </h1>
              <p className="text-xl md:text-2xl text-indigo-200 mb-8">
                {t('blog.hero.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* Search and Filter */}
        <section className="py-12 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="flex flex-col md:flex-row gap-4 mb-8">
                {/* Search */}
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder={t('blog.searchPlaceholder')}
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                </div>
                
                {/* Filter */}
                <div className="md:w-64">
                  <select
                    value={selectedTag}
                    onChange={(e) => setSelectedTag(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="">{t('blog.allTags')}</option>
                    {blogTags.map(tag => (
                      <option key={tag} value={tag}>{tag}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Blog Posts */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              {filteredPosts.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-xl text-gray-600 mb-4">{t('blog.noPostsFound')}</p>
                  <p className="text-gray-500 mb-6">{t('blog.tryDifferentSearch')}</p>
                  <button
                    onClick={() => {
                      setSearchTerm('');
                      setSelectedTag('');
                    }}
                    className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-300"
                  >
                    {t('blog.clearFilters')}
                  </button>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {filteredPosts.map(post => (
                    <article key={post.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition duration-300 overflow-hidden">
                      <Link href={`/blog/${post.slug}`}>
                        <div className="cursor-pointer">
                          <div className="aspect-w-16 aspect-h-9">
                            <img
                              src={post.featuredImage}
                              alt={post.title}
                              className="w-full h-48 object-cover"
                            />
                          </div>
                          <div className="p-6">
                            <div className="flex flex-wrap gap-2 mb-3">
                              {post.tags.map(tag => (
                                <span
                                  key={tag}
                                  className="px-2 py-1 text-xs bg-indigo-100 text-indigo-600 rounded-full"
                                >
                                  {tag}
                                </span>
                              ))}
                            </div>
                            <h2 className="text-xl font-bold mb-3 text-gray-800 hover:text-indigo-600 transition duration-300">
                              {post.title}
                            </h2>
                            <p className="text-gray-600 mb-4 leading-relaxed">
                              {post.excerpt}
                            </p>
                            <div className="flex justify-between items-center text-sm text-gray-500">
                              <time>{new Date(post.publishedAt).toLocaleDateString()}</time>
                              <span>{post.readTime}</span>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </article>
                  ))}
                </div>
              )}
            </div>
          </div>
        </section>

        <Footer />
        <BackToTop />
      </div>
    </>
  );
}