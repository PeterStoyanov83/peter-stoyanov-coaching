import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import BackToTop from '../../components/BackToTop';
import { useTranslation } from '../../hooks/useTranslation';
import { blogPosts } from '../../data/blogPosts';

export default function BlogPost() {
  const router = useRouter();
  const { slug } = router.query;
  const { t } = useTranslation();

  const post = blogPosts.find(p => p.slug === slug);
  
  if (!post) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Post not found</h1>
          <Link href="/blog" className="text-indigo-600 hover:text-indigo-800">
            ← Back to blog
          </Link>
        </div>
      </div>
    );
  }

  const relatedPosts = blogPosts.filter(p => 
    p.id !== post.id && 
    p.tags.some(tag => post.tags.includes(tag))
  ).slice(0, 2);

  return (
    <>
      <Head>
        <title>{post.title} - Peter Stoyanov</title>
        <meta name="description" content={post.excerpt} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white">
        <Header />
        
        {/* Article Header */}
        <article className="pt-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              
              {/* Breadcrumb */}
              <nav className="mb-8">
                <Link href="/blog" className="text-indigo-600 hover:text-indigo-800 flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  {t('blog.backToBlog')}
                </Link>
              </nav>

              {/* Article Meta */}
              <div className="mb-8">
                <div className="flex flex-wrap gap-2 mb-4">
                  {post.tags.map(tag => (
                    <span
                      key={tag}
                      className="px-3 py-1 text-sm bg-indigo-100 text-indigo-600 rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                
                <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4 leading-tight">
                  {post.title}
                </h1>
                
                <div className="flex items-center text-gray-600 space-x-4">
                  <time>{new Date(post.publishedAt).toLocaleDateString()}</time>
                  <span>•</span>
                  <span>{post.readTime}</span>
                  <span>•</span>
                  <span>{t('blog.authorBio')}</span>
                </div>
              </div>

              {/* Featured Image */}
              <div className="mb-12">
                <img
                  src={post.featuredImage}
                  alt={post.title}
                  className="w-full rounded-lg shadow-lg"
                />
              </div>

              {/* Article Content */}
              <div className="prose prose-lg max-w-none mb-12">
                <div 
                  dangerouslySetInnerHTML={{ 
                    __html: post.content.replace(/\n/g, '<br>') 
                  }}
                  className="text-gray-700 leading-relaxed"
                  style={{
                    lineHeight: '1.8'
                  }}
                />
              </div>

              {/* Author Bio */}
              <div className="bg-gray-50 rounded-lg p-8 mb-12">
                <div className="flex items-start space-x-4">
                  <img
                    src="/pictures/PeterStoyanov-straight-look-in-your-eyes.jpg"
                    alt="Peter Stoyanov"
                    className="w-16 h-16 rounded-full object-cover"
                  />
                  <div>
                    <h3 className="font-bold text-lg text-gray-800 mb-2">Peter Stoyanov</h3>
                    <p className="text-gray-600 leading-relaxed">
                      Actor, clown, director, and communication coach with over 20 years of experience 
                      helping people transform their stage presence and communication skills through 
                      theater-based techniques.
                    </p>
                    <div className="mt-4">
                      <Link 
                        href="/about" 
                        className="text-indigo-600 hover:text-indigo-800 font-medium"
                      >
                        Learn more about Peter →
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </article>

        {/* Related Posts */}
        {relatedPosts.length > 0 && (
          <section className="py-12 bg-gray-50">
            <div className="container mx-auto px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl font-bold text-gray-800 mb-8">{t('blog.relatedPosts')}</h2>
                <div className="grid md:grid-cols-2 gap-8">
                  {relatedPosts.map(relatedPost => (
                    <Link key={relatedPost.id} href={`/blog/${relatedPost.slug}`}>
                      <article className="bg-white rounded-lg shadow-md hover:shadow-lg transition duration-300 overflow-hidden cursor-pointer">
                        <img
                          src={relatedPost.featuredImage}
                          alt={relatedPost.title}
                          className="w-full h-32 object-cover"
                        />
                        <div className="p-6">
                          <h3 className="font-bold text-lg text-gray-800 mb-2 hover:text-indigo-600 transition duration-300">
                            {relatedPost.title}
                          </h3>
                          <p className="text-gray-600 text-sm">
                            {relatedPost.excerpt.substring(0, 100)}...
                          </p>
                        </div>
                      </article>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        <Footer />
        <BackToTop />
      </div>
    </>
  );
}