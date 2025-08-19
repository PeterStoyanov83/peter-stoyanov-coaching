import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import BackToTop from '../../components/BackToTop';

export default function BlogPost({ post }) {
  const { t } = useTranslation('common');

  if (!post) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{post.title} | Peter Stoyanov</title>
        <meta name="description" content={post.excerpt} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 py-20 md:py-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <div className="flex justify-center items-center mb-6 space-x-2">
                <span className="text-sm text-blue-200">{post.date}</span>
                {post.tags.length > 0 && (
                  <>
                    <span className="text-white/30">•</span>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {post.tags.map(tag => (
                        <Link key={tag} href={`/blog?tag=${tag}`} className="text-xs bg-yellow-400/20 text-yellow-200 px-2 py-1 rounded-full border border-yellow-400/30 hover:bg-yellow-400/30 transition-colors duration-300">
                          {tag}
                        </Link>
                      ))}
                    </div>
                  </>
                )}
              </div>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                {post.title}
              </h1>
            </div>
          </div>
        </section>

        {/* Blog Content Section */}
        <section className="py-16 md:py-24 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              {/* Featured Image (if available) */}
              {post.featuredImage && (
                <div className="mb-10 rounded-3xl overflow-hidden shadow-2xl border-4 border-white/50">
                  <img 
                    src={post.featuredImage} 
                    alt={post.title} 
                    className="w-full h-auto"
                  />
                </div>
              )}
              
              {/* Blog Content */}
              <article className="prose prose-lg max-w-none bg-white/80 backdrop-blur-sm rounded-3xl p-8 md:p-12 shadow-2xl border border-white/60">
                <div dangerouslySetInnerHTML={{ __html: post.content }} />
              </article>
              
              {/* Author Section */}
              <div className="mt-16 pt-8 bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-2xl border border-white/60">
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full mr-4 flex items-center justify-center text-white font-black text-xl">
                    PS
                  </div>
                  <div>
                    <h3 className="font-black text-gray-900 text-xl">Peter Stoyanov</h3>
                    <p className="text-gray-600 font-medium">{t('blog.authorBio')}</p>
                  </div>
                </div>
                

              </div>
              
              {/* Back to Blog */}
              <div className="mt-12 text-center">
                <Link href="/blog" className="inline-flex items-center px-6 py-3 text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 font-semibold">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  {t('blog.backToBlog')}
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Related Posts Section */}
        {post.relatedPosts && post.relatedPosts.length > 0 && (
          <section className="py-16 md:py-24 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
            <div className="container mx-auto px-4">
              <div className="max-w-6xl mx-auto">
                <h2 className="text-3xl md:text-4xl font-black text-center mb-12 text-white drop-shadow-2xl">
                  {t('blog.relatedPosts')}
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {post.relatedPosts.map((relatedPost) => (
                    <div key={relatedPost.slug} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-3xl overflow-hidden shadow-2xl transition duration-300 hover:shadow-3xl transform hover:scale-105 hover:rotate-1">
                      <Link href={`/blog/${relatedPost.slug}`} className="block">
                        {/* Featured Image */}
                        <div className="h-48 overflow-hidden">
                          {relatedPost.featuredImage ? (
                            <img 
                              src={relatedPost.featuredImage} 
                              alt={relatedPost.title} 
                              className="w-full h-full object-cover transition duration-300 hover:scale-110"
                            />
                          ) : (
                            <div className="w-full h-full bg-gradient-to-br from-indigo-400/20 to-purple-400/20 flex items-center justify-center">
                              <div className="text-white/60">
                                <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                              </div>
                            </div>
                          )}
                        </div>
                        
                        <div className="p-6">
                          <div className="flex items-center mb-3">
                            <span className="text-sm text-blue-200">{relatedPost.date}</span>
                            {relatedPost.tags && relatedPost.tags.length > 0 && (
                              <>
                                <span className="text-white/30 mx-2">•</span>
                                <div className="flex flex-wrap gap-1">
                                  {relatedPost.tags.slice(0, 2).map(tag => (
                                    <span key={tag} className="text-xs bg-yellow-400/20 text-yellow-200 px-2 py-1 rounded-full border border-yellow-400/30">
                                      {tag}
                                    </span>
                                  ))}
                                </div>
                              </>
                            )}
                          </div>
                          <h3 className="text-xl font-black mb-2 text-white drop-shadow-lg line-clamp-2">{relatedPost.title}</h3>
                          <p className="text-white/90 mb-4 line-clamp-3 leading-relaxed">{relatedPost.excerpt}</p>
                          <span className="text-yellow-400 font-semibold">{t('blog.readMore')} →</span>
                        </div>
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}
      </main>

      <Footer />
      <BackToTop />
    </div>
  );
}

export async function getStaticPaths() {
  try {
    // Fetch all published blog posts from backend API
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://peter-stoyanov-backend.onrender.com'}/api/posts?published=true`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch blog posts');
    }
    
    const blogPosts = await response.json();
    
    const paths = blogPosts.map((post) => ({
      params: { slug: post.slug },
    }));

    return { paths, fallback: true };
  } catch (error) {
    console.error('Error fetching blog posts for static paths:', error);
    
    // Return empty paths if API fails, fallback will handle individual requests
    return { paths: [], fallback: true };
  }
}

export async function getStaticProps({ params, locale }) {
  try {
    // Fetch individual blog post from backend API
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://peter-stoyanov-backend.onrender.com'}/api/posts/${params.slug}?language=${locale}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return {
          notFound: true,
        };
      }
      throw new Error('Failed to fetch blog post');
    }
    
    const blogPost = await response.json();
    
    // Fetch related posts
    let relatedPosts = [];
    try {
      const relatedResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://peter-stoyanov-backend.onrender.com'}/api/posts/${params.slug}/related?language=${locale}&limit=3`);
      if (relatedResponse.ok) {
        const relatedData = await relatedResponse.json();
        relatedPosts = relatedData.map(relatedPost => ({
          slug: relatedPost.slug,
          title: relatedPost.title,
          excerpt: relatedPost.excerpt,
          date: relatedPost.published_at ? new Date(relatedPost.published_at).toISOString().split('T')[0] : new Date(relatedPost.created_at).toISOString().split('T')[0],
          featuredImage: relatedPost.featured_image,
          tags: relatedPost.tags || []
        }));
      }
    } catch (relatedError) {
      console.error('Error fetching related posts:', relatedError);
      // Continue without related posts if API fails
    }
    
    // Transform backend data to match frontend format
    const post = {
      slug: blogPost.slug,
      title: blogPost.title,
      content: blogPost.content,
      excerpt: blogPost.excerpt,
      date: blogPost.published_at ? new Date(blogPost.published_at).toISOString().split('T')[0] : blogPost.created_at.split('T')[0],
      tags: blogPost.tags || [],
      featuredImage: blogPost.featured_image,
      language: blogPost.language,
      relatedPosts: relatedPosts
    };

    return {
      props: {
        ...(await serverSideTranslations(locale, ['common'])),
        post
      },
      // Re-generate the page at most once per day
      revalidate: 86400,
    };
  } catch (error) {
    console.error('Error fetching blog post:', error);
    
    // Return 404 if API fails
    return {
      notFound: true,
    };
  }
}