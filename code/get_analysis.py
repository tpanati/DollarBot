import helper
import graphing
from telebot import types
import os

def viewOverallBudget(chat_id, bot):
    if not helper.isCategoryBudgetAvailable(chat_id):
        bot.send_message(chat_id, "No category budget available", reply_markup=types.ReplyKeyboardRemove())
        return
    category_budget = {}
    for cat in helper.getCategoryBudget(chat_id):
        if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
            cat_budget = helper.getCategoryBudgetByCategory(chat_id,cat)
            if cat_budget != '0':
                category_budget[cat] = cat_budget
    print(category_budget,"category budget")
    if category_budget == {}:
        bot.send_message(chat_id,"You are yet to set your budget for different categories.")
    else:
        graphing.overall_split(category_budget)
        bot.send_photo(chat_id, photo=open("overall_split.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
        os.remove("overall_split.png")
        

def viewSpendWise(chat_id, bot):
    category_spend = {}
    for cat in helper.getCategoryBudget(chat_id):
        spend = helper.calculate_total_spendings_for_cateogory_chat_id(chat_id,cat)
        if spend != 0:
            category_spend[cat] = spend

    if category_spend == {}:
        bot.send_message(chat_id, "No expenditure available for this month", reply_markup=types.ReplyKeyboardRemove())
        return
    graphing.spend_wise_split(category_spend)
    bot.send_photo(chat_id, photo=open("spend_wise.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("spend_wise.png")

def viewRemaining(chat_id, bot):
    if not helper.isCategoryBudgetAvailable(chat_id):
        bot.send_message(chat_id, "No category budget available", reply_markup=types.ReplyKeyboardRemove())
        return
    category_spend_percent = {}
    for cat in helper.spend_categories:
        if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
            percent = helper.calculateRemainingCateogryBudgetPercent(chat_id, cat)
            if percent:
                category_spend_percent[cat] = percent
    if category_spend_percent != {}:
        graphing.remaining(category_spend_percent)
        bot.send_photo(chat_id, photo=open("remaining.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
        os.remove("remaining.png")
    else:
        bot.send_message(chat_id,"You are yet to set your budget for different categories.")

def viewHistory(chat_id, bot):
    if not helper.getUserHistory(chat_id):
        bot.send_message(chat_id, "No history available", reply_markup=types.ReplyKeyboardRemove())
        return

    cat_spend_dict = helper.getUserHistoryDateExpense(chat_id)

    graphing.time_series(cat_spend_dict)
    bot.send_photo(chat_id, photo=open("time_series.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("time_series.png")