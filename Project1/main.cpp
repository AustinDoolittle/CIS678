/**
* Project 1: Exploratory Data Analysis
* CIS 678 - Winter 2017
*
* Author: Austin Doolittle
*
**/


#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <set>
#include "gnuplot-iostream.h"

using namespace std;

//Our custom comparer for sorting the analytics data structures
struct CustomGreater {
  template<typename T>
  bool operator() (pair<T, int> const &a, pair<T, int> const &b) const {
    return a.second > b.second;
  }
};

//Computes the Flesch Index based on the given inputs
//
// numSyllables = number of syllables in the document
// numWords = number of words in the document
// numSentences = number of sentences in the document
//
// returns the computer flesch index
double ComputeFleschIndex(int numSyllables, int numWords, int numSentences) {
  return 206.835 - 84.6 * ((double)numSyllables / numWords) - 1.015 * ((double)numWords / numSentences);
}

//Constant to control how many words to display on word Frequency graph
int const WORD_FREQ_COUNT = 20;

int main() {
  string filename;
  string word;
  int wordcount, sentenceCount, syllableTotalCount, sentenceLength;
  map<int, int> syllableFreq;
  map<int, int> sentenceLengthFreq;
  map<string, int> wordFreq;
  Gnuplot gp;

  //set precision output
  cout.precision(5);

  //set up Gnuplot
  gp << "set term png\n";
  gp << "set boxwidth 0.5\n";
  gp << "set style fill solid\n";
  gp << "set xrange [0:10]\nset yrange [0:10]\n";
  gp << "set autoscale xmax\nset autoscale ymax\n";
  gp << "set key off\n";

  //enter loop
  while(true) {
    //make sure all variables are initialized since last loop
    syllableFreq.clear();
    sentenceLengthFreq.clear();
    wordFreq.clear();
    wordcount = 0; sentenceCount = 0; syllableTotalCount = 0; sentenceLength = 0;

    //Get the filename to read from
    cout << "Please enter a filename (q to quit): ";
    cin >> filename;

    //check for user quit
    if(filename == "q") {
      break;
    }

    //open file, check for error
    ifstream file(filename.c_str());
    if(!file) {
      cout << "File could not be opened: " << strerror(errno) << endl << endl;
      continue;
    }
    cout << endl;

    //print initial line that will be replaced during the loop
    cout << "Words: " << wordcount << "\tSentences: " << sentenceCount << "\tSyllables: " << syllableTotalCount;

    //loop over every word in the file and calculate words, sentences, and syllables
    while(file >> word) {
      //increment word counts
      wordcount++;
      sentenceLength++;

      int sCount = 0;
      bool wasLastVowel = true;
      bool isAlphaNumeric = false;

      //loop over each character in the extracted word
      for(int i = 0; i < word.size(); i++) {
        //convert to lowercase
        word[i] = tolower(word[i]);

        //check if it is a vowel
        if((word[i] == 'e' && i != (word.size() - 1)) || word[i] == 'a' || word[i] == 'o' || word[i] == 'i' || word[i] == 'u' || word[i] == 'y') {
          //first character or last was consonant
          if(i == 0 || !wasLastVowel) {
            sCount++;
          }
          wasLastVowel = true;
        }
        else {
          wasLastVowel = false;
        }

        //set the flag that alerts to nonwords
        if(isalnum(word[i])) {
          isAlphaNumeric = true;
        }

        //check if we are at the last character
        if (i == (word.size() - 1)) {
          //if this character is puncuation and the sentence is made up of at least 1 word, this word is at the end of a sentence
          if((word[i] == '.' || word[i] == '?' || word[i] == '!') && (sentenceLength != 1 || isAlphaNumeric)) {
            sentenceCount++;
            sentenceLengthFreq[sentenceLength]++;
            sentenceLength = 0;

            //remove the last character for analytics
            word.erase(i);
          }
        }
      }

      //only add to analytical data if this was actually a word
      if(isAlphaNumeric) {
        wordFreq[word]++;
        syllableTotalCount += sCount;
        syllableFreq[sCount]++;
      }

      //print out statistics
      cout << "\rWords: " << wordcount << "\tSentences: " << sentenceCount << "\t Syllables: " << syllableTotalCount;
    }
    cout << endl;

    //compute flesch index
    double fleschIndex = ComputeFleschIndex(syllableTotalCount, wordcount, sentenceCount);
    cout << "Flesch Index = " << fleschIndex << endl;

    //print out evaluation of flesch Index
    cout << "Reading Level: ";
    if(fleschIndex <= 30.0) {
      cout << "College Graduate";
    }
    else if(fleschIndex <= 50.0) {
      cout << "College";
    }
    else if(fleschIndex <= 60.0) {
      cout << "10th to 12th Grade";
    }
    else if(fleschIndex <= 70.0) {
      cout << "8th & 9th Grade";
    }
    else if(fleschIndex <= 80.0) {
      cout << "7th Grade";
    }
    else if(fleschIndex <= 90.0) {
      cout << "6th Grade";
    }
    else if(fleschIndex <= 100.0) {
      cout << "5th Grade";
    }
    else {
      cout << "< 5th Grade";
    }
    cout << endl << endl;

    file.close();

    //begin analytics

    string filenameOnly = filename.substr(0, filename.find_last_of("."));

    //word Frequency
    //get vector of words and their counts
    vector<pair<string,int>> wordFreqVect1;
    for(auto tup : wordFreq) {
      wordFreqVect1.push_back(tup);
    }

    //sort based on our custom comparer
    sort(wordFreqVect1.begin(), wordFreqVect1.end(), CustomGreater());

    //get new vector of top WORD_FREQ_COUNT values, add an index for plotting
    vector<tuple<int, string, int>> wordFreqVect2;
    for(int i = 0; i < wordFreqVect1.size() && i < WORD_FREQ_COUNT; i++) {
      wordFreqVect2.push_back(make_tuple((i*2) + 1, wordFreqVect1[i].first, wordFreqVect1[i].second));
    }

    cout << "Plotting Word Frequencies to " << filenameOnly << "_wordFreq.png" << endl;
    gp << "set output '" << filenameOnly << "_wordFreq.png'\n";
    gp << "set xlabel 'Words'\nset ylabel 'Frequency'\n";
    gp << "set title 'Word Frequency'\n";
    gp << "plot '-' using 1:3:xtic(2) with boxes\n";
    gp.send1d(wordFreqVect2);

    //syllableFreq
    //push syllable count frequencies to vector, maintain map order based on key
    vector<pair<int,int>> syllableFreqVect;
    int last = 0;
    for(auto it = syllableFreq.begin(); it != syllableFreq.end(); ++it) {
      //fill in gaps where no counts exist for aesthetics
      for(int i = last + 1; i < (*it).first; i++) {
        syllableFreqVect.push_back(make_pair(i, 0));
      }
      syllableFreqVect.push_back(*it);
    }

    cout << "Plotting Syllable Count Frequencies to " << filenameOnly << "_syllFreq.png" << endl;
    gp << "set output '" << filenameOnly << "_syllFreq.png'\n";
    gp << "set xlabel 'Syllable Counts'\nset ylabel 'Frequency'\n";
    gp << "set title 'Syllable Frequency'\n";
    gp << "plot '-' using 1:2:xtic(1) with boxes\n";
    gp.send1d(syllableFreqVect);

    //sentenceLengthFreq
    //push sentence length frequencies to vector for plotting, maintain map order
    vector<pair<int,int>> sentenceLengthFreqVect;
    last = 0;
    for(auto it = sentenceLengthFreq.begin(); it != sentenceLengthFreq.end(); ++it) {
      //fill in gaps where no counts exist for aesthetics
      for(int i = last + 1; i < (*it).first; i++) {
        sentenceLengthFreqVect.push_back(make_pair(i, 0));
      }
      sentenceLengthFreqVect.push_back(*it);
      last = (*it).first;
    }

    cout << "Plotting Sentence Length Frequencies to " << filenameOnly << "_senlenFreq.png" << endl << endl;
    gp << "set output '" << filenameOnly << "_senlenFreq.png'\n";
    gp << "set xlabel 'Sentence Length'\nset ylabel 'Frequency'\n";
    gp << "set title 'Sentence Length Frequency'\n";
    gp << "plot '-' using 1:2:xtic(1) with boxes\n";
    gp.send1d(sentenceLengthFreqVect);
  }

  cout << "Goodbye" << endl;
  exit(0);
}
