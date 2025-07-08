import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../../components/Header';
import Footer from '../../components/Footer';

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
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gray-50 py-20 md:py-32">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <div className="flex justify-center items-center mb-6 space-x-2">
                <span className="text-sm text-gray-500">{post.date}</span>
                {post.tags.length > 0 && (
                  <>
                    <span className="text-gray-300">•</span>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {post.tags.map(tag => (
                        <Link key={tag} href={`/blog?tag=${tag}`} className="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full">
                          {tag}
                        </Link>
                      ))}
                    </div>
                  </>
                )}
              </div>
              <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                {post.title}
              </h1>
            </div>
          </div>
        </section>

        {/* Blog Content Section */}
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              {/* Featured Image (if available) */}
              {post.featuredImage && (
                <div className="mb-10 rounded-xl overflow-hidden shadow-lg">
                  <img 
                    src={post.featuredImage} 
                    alt={post.title} 
                    className="w-full h-auto"
                  />
                </div>
              )}
              
              {/* Blog Content */}
              <article className="prose prose-lg max-w-none">
                <div dangerouslySetInnerHTML={{ __html: post.content }} />
              </article>
              
              {/* Author Section */}
              <div className="mt-16 pt-8 border-t border-gray-200">
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-gray-300 rounded-full mr-4"></div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Peter Stoyanov</h3>
                    <p className="text-gray-600">{t('blog.authorBio')}</p>
                  </div>
                </div>
              </div>
              
              {/* Back to Blog */}
              <div className="mt-12 text-center">
                <Link href="/blog" className="inline-flex items-center text-indigo-600 font-medium">
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
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
                {t('blog.relatedPosts')}
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {post.relatedPosts && post.relatedPosts.map((relatedPost) => (
                  <div key={relatedPost.slug} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-md transition duration-300 hover:shadow-lg">
                    <Link href={`/blog/${relatedPost.slug}`} className="block">
                      {/* If you have featured images, add them here */}
                      <div className="h-48 bg-gray-200"></div>
                      
                      <div className="p-6">
                        <div className="flex items-center mb-2">
                          <span className="text-sm text-gray-500">{relatedPost.date}</span>
                        </div>
                        <h3 className="text-xl font-semibold mb-2 text-gray-900">{relatedPost.title}</h3>
                        <p className="text-gray-600 mb-4">{relatedPost.excerpt}</p>
                        <span className="text-indigo-600 font-medium">{t('blog.readMore')} →</span>
                      </div>
                    </Link>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export async function getStaticPaths() {
  // In a real app, you would fetch all posts from your API
  // For now, we'll use dummy data
  const posts = [
    { slug: 'mastering-public-speaking' },
    { slug: 'voice-projection-tips' },
    { slug: 'body-language-secrets' },
    { slug: 'overcoming-stage-fright' },
    { slug: 'storytelling-for-business' },
    { slug: 'breathing-techniques' }
  ];

  const paths = posts.map((post) => ({
    params: { slug: post.slug },
  }));

  return { paths, fallback: true };
}

export async function getStaticProps({ params, locale }) {
  // In a real app, you would fetch this from your API
  // For now, we'll use dummy data
  const posts = {
    'mastering-public-speaking': {
      slug: 'mastering-public-speaking',
      title: 'Mastering Public Speaking: 5 Theater Techniques That Work',
      content: `
        <p>Public speaking is often cited as one of the most common fears people have. Yet, with the right techniques, anyone can become a confident and engaging speaker. As an actor and coach with over 20 years of experience, I've found that theater techniques offer powerful tools for improving public speaking skills.</p>
        
        <h2>1. The Power of Breath Control</h2>
        <p>Actors understand that breath is the foundation of vocal projection and emotional control. Before going on stage, practice deep diaphragmatic breathing: inhale slowly through your nose for a count of four, hold for two, and exhale through your mouth for six. This technique calms nerves and provides the breath support needed for clear, powerful speech.</p>
        
        <h2>2. Physical Grounding</h2>
        <p>Theater performers know that stance and posture affect both how you feel and how others perceive you. Stand with your feet shoulder-width apart, weight evenly distributed. Feel your connection to the ground. This "power stance" increases confidence and projects authority to your audience.</p>
        
        <h2>3. Vocal Variety</h2>
        <p>Monotone delivery will lose your audience quickly. Practice varying your pitch, pace, and volume. Try reading the same sentence as a question, an excited statement, and a solemn declaration. This flexibility makes your speech more engaging and helps emphasize key points.</p>
        
        <h2>4. The Pause</h2>
        <p>One of the most powerful tools in theater is the strategic pause. Many speakers rush through their material, but well-placed pauses give the audience time to absorb important points and create dramatic emphasis. Don't be afraid of silence – it's often more powerful than words.</p>
        
        <h2>5. Character Work</h2>
        <p>When nervous, try thinking of your presentation as a performance. Create a slightly more confident "character" version of yourself. This mental shift can help separate personal anxiety from the task at hand, allowing you to present with greater ease.</p>
        
        <p>These theater-based techniques have helped countless professionals transform their public speaking abilities. Remember that like any skill, improvement comes with practice. Start incorporating these approaches into your presentations, and you'll soon find yourself speaking with greater confidence and impact.</p>
      `,
      excerpt: 'Learn how theater techniques can transform your public speaking skills and help you connect with any audience.',
      date: '2023-05-15',
      tags: ['public-speaking', 'theater'],
      relatedPosts: [
        {
          slug: 'voice-projection-tips',
          title: 'Voice Projection Tips for Effective Communication',
          excerpt: 'Discover how to use your voice effectively to command attention and convey your message with impact.',
          date: '2023-04-22'
        },
        {
          slug: 'body-language-secrets',
          title: 'Body Language Secrets from Professional Actors',
          excerpt: 'Explore how professional actors use body language to enhance their performances and how you can apply these techniques.',
          date: '2023-03-10'
        },
        {
          slug: 'overcoming-stage-fright',
          title: 'Overcoming Stage Fright: A Step-by-Step Guide',
          excerpt: 'Learn practical techniques to manage anxiety and perform confidently in front of any audience.',
          date: '2023-02-18'
        }
      ]
    },
    'voice-projection-tips': {
      slug: 'voice-projection-tips',
      title: 'Voice Projection Tips for Effective Communication',
      content: `<p>Your voice is one of your most powerful tools for communication. Whether you're speaking to a small group or addressing a large audience, how you use your voice can make the difference between engaging listeners and losing their attention.</p>
      
      <h2>Understanding Voice Projection</h2>
      <p>Voice projection isn't about shouting—it's about producing a clear, resonant sound that carries well. It involves proper breath support, vocal placement, and articulation.</p>
      
      <h2>Breath Support: The Foundation</h2>
      <p>All good voice work begins with proper breathing. Practice diaphragmatic breathing by placing your hand on your abdomen and ensuring it expands when you inhale. This provides the air support needed for strong projection.</p>
      
      <h2>Finding Resonance</h2>
      <p>To add richness to your voice, focus on creating resonance in your chest, throat, and facial cavities. Try humming at different pitches to feel where your voice resonates most naturally.</p>
      
      <h2>Articulation Exercises</h2>
      <p>Clear articulation ensures your words are understood. Practice tongue twisters daily to improve the precision of your consonants and the clarity of your vowels.</p>
      
      <h2>Varying Your Delivery</h2>
      <p>A dynamic voice keeps listeners engaged. Experiment with changing your pace, pitch, and volume to emphasize important points and create interest.</p>
      
      <h2>Practical Tips for Daily Practice</h2>
      <p>Spend 10 minutes each day on vocal exercises. Record yourself speaking and listen critically. Practice projecting to the back of a room without straining your voice.</p>
      
      <p>Remember, a well-projected voice communicates confidence and authority. With consistent practice of these techniques, you'll develop a voice that commands attention and effectively conveys your message.</p>`,
      excerpt: 'Discover how to use your voice effectively to command attention and convey your message with impact.',
      date: '2023-04-22',
      tags: ['voice', 'communication'],
      relatedPosts: [
        {
          slug: 'mastering-public-speaking',
          title: 'Mastering Public Speaking: 5 Theater Techniques That Work',
          excerpt: 'Learn how theater techniques can transform your public speaking skills and help you connect with any audience.',
          date: '2023-05-15'
        },
        {
          slug: 'breathing-techniques',
          title: 'Breathing Techniques for Better Speech and Presence',
          excerpt: 'Master the art of breathing to improve your vocal quality, reduce stress, and enhance your overall presence.',
          date: '2022-12-12'
        },
        {
          slug: 'body-language-secrets',
          title: 'Body Language Secrets from Professional Actors',
          excerpt: 'Explore how professional actors use body language to enhance their performances and how you can apply these techniques.',
          date: '2023-03-10'
        }
      ]
    }
    // Other posts would be defined here
  };

  const post = posts[params.slug];

  // If the post doesn't exist, return 404
  if (!post) {
    return {
      notFound: true,
    };
  }

  return {
    props: {
      ...(await serverSideTranslations(locale, ['common'])),
      post
    },
    // Re-generate the page at most once per day
    revalidate: 86400,
  };
}