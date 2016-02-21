#!/usr/bin/env ruby

require 'socket'
require './flag.rb'

server = TCPServer.new 12037
loop do
  Thread.start(server.accept) do |client|
    client.puts "Let me count the ascii values of 10 characters:"
    input = client.recv(100).strip
    
    if not /^[a-f]{10}$/ =~ input
    	client.puts "WRONG!!!! Only 10 characters matching /^[a-f]{10}$/ !"
    	client.close
    end

    sum = 0
    input.chars.each do |c|
    	sum += c.ord
    end
    client.puts "Sum is: #{sum}"

    max = "f".ord * 10
    
    if sum > max
    	client.puts FLAG
    else
    	client.puts "That's not enough (#{sum} < #{max}) :("
    end

    client.close
  end
end
