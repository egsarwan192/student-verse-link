
import React from 'react';
import { Link } from 'react-router-dom';

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-white to-orange-100">
      <div className="text-center max-w-4xl px-4 py-16">
        <h1 className="text-5xl font-bold mb-6 text-gray-800">Connect, Discover, Succeed</h1>
        <p className="text-xl text-gray-600 mb-8">
          The platform that connects students and colleges for a brighter future
        </p>
        
        <div className="bg-white p-8 rounded-lg shadow-lg mb-10 max-w-3xl mx-auto">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">About Campus Connect</h2>
          <p className="text-gray-600 mb-6">
            Campus Connect is a revolutionary platform designed to bridge the gap between students and educational institutions. 
            Our mission is to create a vibrant ecosystem where students can discover opportunities, colleges can showcase their unique offerings, 
            and meaningful connections can flourish.
          </p>
          
          <div className="grid md:grid-cols-3 gap-6 mb-6">
            <div className="bg-orange-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-orange-600 mb-2">For Students</h3>
              <p className="text-gray-600">Build your profile, explore colleges, connect with peers, and discover events and opportunities.</p>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-orange-600 mb-2">For Colleges</h3>
              <p className="text-gray-600">Showcase your campus, promote events, connect with prospective students, and build your community.</p>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-orange-600 mb-2">Community</h3>
              <p className="text-gray-600">Join a growing network of students and institutions collaborating for academic excellence.</p>
            </div>
          </div>
        </div>
        
        <div className="mb-8">
          <h3 className="text-xl mb-4 text-gray-700">I am a:</h3>
          <div className="flex justify-center space-x-4 mb-3">
            <button className="bg-orange-500 text-white px-8 py-3 rounded-full hover:bg-orange-600 transition">
              Student
            </button>
            <button className="bg-gray-200 text-gray-800 px-8 py-3 rounded-full hover:bg-gray-300 transition">
              College
            </button>
          </div>
        </div>
        
        <div className="flex justify-center space-x-6">
          <Link to="/login" className="bg-orange-500 text-white px-8 py-3 rounded-full hover:bg-orange-600 transition">
            Get Started
          </Link>
          <button className="border-2 border-orange-500 text-orange-500 px-8 py-3 rounded-full hover:bg-orange-50 transition">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
};

export default Index;
