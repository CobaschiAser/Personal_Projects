import matplotlib.pyplot as plt

import matplotlib.pyplot as plt


def plot(results):
    fig, ax = plt.subplots()

    bars = ax.bar(results.keys(), results.values(), color=['blue', 'green', 'red'])

    ax.set_ylabel('Accuracy')
    ax.set_ylim(0, 1)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.3f}', ha='center', va='bottom')

    plt.show()


if __name__ == "__main__":
    results_bayes_naive = {
        "Flip_coin_accuracy": 0.49398625429553267,
        "Always_zero_accuracy": 0.8316151202749141,
        "Bayes_Naive_accuracy": 0.9896907216494846
    }
    results_knn = {
        "Flip_coin_accuracy": 0.49398625429553267,
        "Always_zero_accuracy": 0.8316151202749141,
        "KNN_accuracy": 0.8419243986254296
    }
    results_bonus = {
        "Flip_coin_accuracy": 0.49398625429553267,
        "Always_zero_accuracy": 0.8316151202749141,
        "Bonus_accuracy": 0.9904926534140017
    }
    results_bayes_naive_cvloo = {
        "part1": 0.9896551724137931,
        "part2": 0.9835640138408305,
        "part3": 0.9896193771626297,
        "part4": 0.986159169550173,
        "part5": 1.0,
        "part6": 1.0,
        "part7": 0.9922145328719724,
        "part8": 0.9801038062283737,
        "part9": 0.9887543252595156,
        "part10": 0.9896907216494846,
        "cvloo": 0.9899761118976773
    }
    results_knn_cvloo = {
        "part1": 0.8375,
        "part2": 0.8416955017301038,
        "part3": 0.8451557093425606,
        "part4": 0.8442906574394463,
        "part5": 0.8491379310344828,
        "part6": 0.8512110726643599,
        "part7": 0.842560553633218,
        "part8": 0.8416955017301038,
        "part9": 0.8538062283737025,
        "part10": 0.8419243986254296,
        "cvloo": 0.8448977554573409
    }
    results_bonus_cvloo = {
        "part3": 1.0,
        "part4": 0.9975990396158463,
        "part5": 1.0,
        "part6": 1.0,
        "part7": 0.9968017057569296,
        "part8": 0.9834710743801653,
        "part9": 0.9960435212660732,
        "part10": 0.9904926534140017,
        "cvloo": 0.995550999304127
    }

    results_bayes_vs_knn = {
        "Flip_coin": 0.49398625429553267,
        "Always_zero": 0.8316151202749141,
        "BN_acc": 0.9896907216494846,
        "KNN_acc": 0.8419243986254296,
        "BN_cvloo": 0.9899761118976773,
        "KNN_cvloo": 0.8448977554573409
    }

    # plot(results_bayes_naive)
    # plot(results_knn)
    # plot(results_bayes_naive_cvloo)
    # plot(results_knn_cvloo)
    # plot(results_bonus)
    plot(results_bonus_cvloo)
    # plot(results_bayes_vs_knn)
