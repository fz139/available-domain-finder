#!/usr/bin/env ruby

require 'whois-parser'

if ARGV.length != 2
    puts "Usage: test.rb <domainlist> <result>\n"
    exit
end

filename=ARGV[0]
resultfile=ARGV[1]

File.open(resultfile, 'w') do |f|
        File.open(filename, "r").each_line do |line|
                begin
                        record = Whois.whois(line.chomp!)
                        parser = record.parser
                        if parser.available? then
                                #puts line
                                f.puts line
                                f.flush
                                sleep 2
                        end
                rescue => exception
                       puts "error: " + line + " #{exception}"
                end
        end
end
