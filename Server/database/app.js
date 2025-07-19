const express = require('express');
const mongoose = require('mongoose');
const Dealership = require('./models/dealership');
const Review = require('./models/review');

const app = express();
const port = process.env.PORT || 3030;

app.use(express.json());

mongoose.connect('mongodb://mongodb:27017/dealerships', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('MongoDB connected successfully'))
.catch(err => console.error('MongoDB connection error:', err));

app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealership.find({});
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealers = await Dealership.find({ state: req.params.state });
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealership.findById(req.params.id);
    if (!dealer) {
      return res.status(404).json({ message: 'Dealer not found' });
    }
    res.json(dealer);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get('/fetchReviews', async (req, res) => {
  try {
    const reviews = await Review.find({});
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const reviews = await Review.find({ dealership: req.params.id });
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.post('/insertReview', async (req, res) => {
  try {
    const { dealership, name, purchase, review, purchase_date, car_make, car_model, car_year } = req.body;

    const newReview = new Review({
      dealership: dealership,
      name: name,
      purchase: purchase,
      review: review,
      purchase_date: purchase_date,
      car_make: car_make,
      car_model: car_model,
      car_year: car_year,
    });

    await newReview.save();
    res.status(201).json(newReview);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

app.listen(port, () => {
  console.log(`Express server listening at http://localhost:${port}`);
});